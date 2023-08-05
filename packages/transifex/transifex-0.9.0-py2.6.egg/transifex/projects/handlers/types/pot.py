# -*- coding: utf-8 -*-
import os
import polib
import itertools
from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal
from translations.lib.types.pot import POTManager
from translations.models import POFile
from languages.models import Language
from txcommon.log import logger
from txcommon import rst
from projects.models import Component
from projects.signals import pre_set_stats, post_set_stats
from vcs.lib.exceptions import RevisionRepoError

class POTHandler:
    """
    POTManager abstraction layer, specific to the projects app.

    You can use this higher-level object to interact with a
    component's statistics instead of meddling with the lower-
    level POTManager. Each Component object gets one of these
    as ``component.trans``.

    """
    def __init__(self, component):
        self.component = component
        # TODO: Make Unit init the browser on its own 
        component.unit._init_browser()
        browser = component.unit.browser
        self.tm = POTManager(component.full_name, browser.path, 
            component.source_lang, component.file_filter)

        # It stores a mapping of source files intended to be used to find out
        # if the related POT of a PO file has changed. If it has changed, the
        # PO should be merged and the stats recalculated for it.
        # This dict var is filled whenever the set_file_stat is called with 
        # is_pot=True. It's usually done only by the set_source_stats, that is 
        # called by set_stats, which is used to calculate the stats for the
        # whole component of a project.
        self.SOURCE_MAP = {}

    def get_manager(self):
        return self.tm

    def set_file_stats(self, filename, is_msgmerged=True, is_pot=False):
        """Set the statistics of a specificy file for an object."""

        ctype = ContentType.objects.get_for_model(self.component)
        s, created = POFile.objects.get_or_create(object_id=self.component.id,
            content_type=ctype, filename=filename, is_pot=is_pot)

        logger.debug("Setting stats for %s." % s.filename)

        if created:
            logger.debug("POFile has been created.")
        else:
            logger.debug("POFile already existed.")

        if not is_pot:
            lang_code = self.guess_language(filename)
            logger.debug("Guessed language is '%s'." % lang_code)
            if not s.language:
                try:
                    l = Language.objects.by_code_or_alias(code=lang_code)
                    s.language=l
                except Language.DoesNotExist:
                    logger.debug("No language found for the '%s' language " \
                        "code." % lang_code)

            s.language_code = lang_code

        calcstats = True
        rev = None
        if hasattr(self.component, 'get_rev'):
            try:
                rev = self.component.get_rev(filename)
            except RevisionRepoError:
                pass

            if rev and rev == s.rev:
                calcstats = False
            else:
                logger.debug("VCS revision for the file has changed.")

        # If POFile is enabled=False we must enforce the stats calculation
        if not s.enabled:
            calcstats, s.enabled = True, True
            logger.debug("POFile had attr 'enabled=False'.")

        # For intltool components that the pot file has changes, it's
        # necessary to recalc the stats even if the 'rev' is the same
        # FIXME: It's too tied
        elif self.component.i18n_type=='INTLTOOL' and (is_msgmerged or is_pot):
            calcstats = True
            logger.debug("It's an intltool component with POT changes.")

        if is_pot:
            self.SOURCE_MAP.update({filename:calcstats})
            source_file, source_changed = None, False
        else:
            source_file = self.tm.get_source_file_for_pofile(filename)
            logger.debug("Related source file: %s" % source_file)
            source_changed = self.SOURCE_MAP.get(source_file, False)
            logger.debug("Source file changed? %s." % source_changed)

        if calcstats or source_changed:
            stats = self.tm.calculate_file_stats(filename, source_file,
                is_msgmerged)
            s.set_stats(trans=stats['trans'], fuzzy=stats['fuzzy'], 
                untrans=stats['untrans'], error=stats['error'])
            s.is_msgmerged = stats['is_msgmerged']
            if rev:
                s.rev = rev
        else:
            logger.debug("No need to re-calculate stats.")
        return s.save()

    def set_stats_base(self, is_msgmerged=True, is_pot=False):
        """Set the source file (pot) in the database"""
        if is_pot:
            files = self.tm.get_source_files()
        else:
            files = self.tm.get_po_files()
        for filename in files:
            self.set_file_stats(filename, is_msgmerged, is_pot)

    def set_source_stats(self, is_msgmerged):
        """Set the stats for source files (pot) in the database."""
        logger.debug("Calc stats for the source files of %s" % self.component)
        self.set_stats_base(is_msgmerged, is_pot=True)

    def set_po_stats(self, is_msgmerged):
        """Set the stats for po files (po) in the database"""
        logger.debug("Calc stats for the translation files of %s" % self.component)
        self.set_stats_base(is_msgmerged, is_pot=False)

    def set_lang_stats(self, lang_code, is_msgmerged=True):
        """Set stats for a specificy language."""
        for filename in self.tm.get_lang_files(lang_code):
            self.set_file_stats(filename, is_msgmerged, False)

    def set_stats(self):
        """Calculate stats for all translations of the component."""

        logger.debug("Setting stats for %s" % self.component)

        Signal.send(pre_set_stats, sender=Component,
                    instance=self.component)
        # Copying the source file to the static dir
        potfiles = self.tm.get_source_files()
        if potfiles:
            is_msgmerged=True
            for potfile in potfiles:
                self.tm.copy_file_to_static_dir(potfile)
        else:
            # TODO: There is no source file (POT)
            # It looks like an intltool POT-based, what should we do?
            is_msgmerged=False

        # Making sure the mapping is empty. Here is where it is actually used.
        # As set_source_stats and set_po_stats are called here in serial, it 
        # fills the SOURCE_MAP and then the next method uses it to know what 
        # POTs have changed and do whatever is needed based on it.
        self.SOURCE_MAP = {}
        self.set_source_stats(is_msgmerged=False)
        self.set_po_stats(is_msgmerged)

        self.clean_old_stats()
        Signal.send(post_set_stats, sender=Component,
                    instance=self.component)

    def get_stats(self):
        """Return stats for the component from the database."""
        return POFile.objects.by_object_total(self.component)

    def get_rest_stats(self):
        """Return stats for the component as a restructured text table."""
        pofiles = self.get_stats()
        stats = [[po.lang_or_code, po.trans_perc] for po in pofiles]
        # Sorting the list of lists according to the second column, the completion
        stats.sort(lambda x,y:cmp(x[1],y[1]), reverse=True)
        #Add % simboly to the completion column after sorting it
        stats = [[x, '%d%%' % y] for x, y in stats]
        return rst.as_table([['Language', 'Completion']] + stats)

    def get_lang_stats(self, lang_code):
        """Return stats of the component in a specific language from the database."""
        return POFile.objects.by_lang_code_and_object(lang_code, self.component)

    def get_source_stats(self):
        """Return the source file (pot) stats from the database."""
        try:
            return POFile.objects.by_object(self.component).filter(
                is_pot=True).order_by('filename')
        except POFile.DoesNotExist:
            return None

    def get_po_stats(self, po_contents):
        """
        Abstraction for getting a dictionary with the stats for a POT/PO 
        file content.
        """
        return self.tm.get_po_stats(po_contents)

    def get_stats_completion(self, stats):
        """Abstraction for getting the completion of a po file stats disctionaty."""
        return self.tm.get_stats_completion(stats)

    def get_stats_status(self, stats):
        """Abstraction for getting the status of the stats completion."""
        return self.tm.get_stats_status(stats)

    def get_file_contents(self, filename, is_msgmerged):
        """Abstraction for getting the contents of a filename."""
        return self.tm.get_file_contents(filename, is_msgmerged)

    def get_po_entries(self, filename):
        """Abstration for getting a polib.POFile with the entries of filename."""
        return self.tm.get_po_entries(filename)

    def get_source_file(self):
        """Abstration for getting source files."""
        return self.tm.get_source_file()

    def clean_stats(self):
        """
        Set all stats of translations for the component in the database as
        enabled=False.

        POFiles with enabled=False do not appear at the UI.
        """
        logger.debug("Cleaning stats for %s" % self.component)
        POFile.objects.by_object(self.component).update(enabled=False)

    def clean_old_stats(self):
        """
        Clean old stats present on the database and msgmerge directory.

        Useful for removing files that are not present in the upstream 
        repository anymore.

        """
        logger.debug("Cleaning old stats for %s" % self.component)
        files = itertools.chain(self.tm.get_source_files(), 
            self.tm.get_po_files())
        pofiles = POFile.objects.select_related().filter(
            component=self.component).exclude(filename__in=list(files))
        for stat in pofiles:
            logger.debug("Cleaning '%s'" % stat.filename)
            self.tm.delete_file_from_static_dir(stat.filename)
            stat.delete()

    def guess_language(self, filename):
        """Abstraction for guessing a language code from a filename."""
        return self.tm.guess_language(filename)

    def msgfmt_check(self, po_contents):
        """Abstraction for POT/PO file checking with 'msgfmt -c'."""
        return self.tm.msgfmt_check(po_contents)


