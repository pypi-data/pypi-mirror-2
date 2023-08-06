# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile
from polib import pofile
from django.conf import settings
from django.utils.translation import ugettext as _
from django_addons.errors import AddonError
from txcommon.log import logger
from projects.signals import pre_submit_file, post_submit_file
from projects.models import Component
from translations.lib.types.pot import FileFilterError, MsgfmtCheckError
from errors import SubmitError

def pobuffer(buf):
    """
    Function to generate polib.pofile() from string
    """
    fh = NamedTemporaryFile()
    fh.write(buf)
    fh.flush()
    po = pofile(fh.name)
    fh.close() # Delete temporary file
    return po
    
def pre_submit_check(sender, instance=None, user=None, component=None,
    stream=None, filename=None, file_dict=None,  **kwargs):
    # Sanity checks
    if not component or not stream or not user or not filename:
        raise SubmitError("'component', 'filename', 'stream' or 'user' "
            " not specified for pre_submit_file handler!")

    # (6.3) Reject access to POT files, actually anything that isn't *.po
    # Note that stream.name is the filename what user has uploaded
    if settings.PRESUBMIT_CHECK_ALLOW_PO_ONLY:
        if not stream.name.lower().endswith(".po"):
            raise SubmitError(_("You are only allowed to upload PO files (*.po)!"))

    # (6.1) Empty file check
    if stream.size == 0:
        raise SubmitError(_("You have submitted empty file!"))

    # Read the stream to buffer
    buf = stream.read()

    # (6.4) Check wether file containts DOS newlines '\r' (0x0D)
    # To remove you can run: tr -d '\r' < inputfile > outputfile
    if settings.PRESUBMIT_CHECK_DOS_NEWLINES:
        if '\r' in buf:
            raise SubmitError(_("Uploaded file contains "
                "DOS newlines (\\r)!"))

    # Open POFile on the buffer
    po = pobuffer(buf)

    # (6.5.2) Check required header fields 
    required_fields = ['Plural-Forms', 'Content-Type', 
        'Content-Transfer-Encoding']
    for field in required_fields:
        if not "Content-Type" in po.metadata:
            raise SubmitError(_("Uploaded file header doesn't "
               "have '%s' field!") % field)

    # (6.5.1) Check charset in header (UTF-8)
    if settings.PRESUBMIT_CHECK_UTF8:
        if not "charset=utf-8" in po.metadata["Content-Type"].lower():
            raise SubmitError(_("Only UTF-8 encoded files are allowed!"))

    # (6.1) No translated entires check
    if len(po.translated_entries()) + len(po.fuzzy_entries()) < 1:
        raise SubmitError(_("Uploaded file doesn't contain any "
            "translated entries!"))


    # Msgfmt check
    if settings.PRESUBMIT_CHECK_MSGFMT:
        try:
            stream.seek(0)
            component.trans.msgfmt_check(stream)
        except MsgfmtCheckError:
            logger.debug("Msgfmt -c check failed for file %s." % filename)
            if (hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST and
                user.email):
                from submissions.utils import msgfmt_error_send_mail
                msgfmt_error_send_mail(component, user, stream, file_dict,
                    filename)
                user.message_set.create(message=_(
                    "Your file has been e-mailed to you to avoid "
                    "loss of any work."))
            else:
                user.message_set.create(message=_(
                    "We couldn't send you an email to preserve "
                    "your work because you haven't registered an "
                    "email address."))
            raise SubmitError("Your file does not pass the correctness checks"
                " (msgfmt -c). Please run this command on your system to "
                "see the errors.")

def connect():
    pre_submit_file.connect(pre_submit_check, sender=Component)