import os, re
import polib
from django.conf import settings
from translations.lib.types import (TransManagerMixin, TransManagerError)
from txcommon.commands import (run_command, CommandError)
from txcommon.log import logger

# Reusable regex for languages, to be inserted in the re list elements.
# We are excluding the match 'po' in order to be more flexible with
# the matching below (thanks to #regex folks Accolate/ackana)
LANG_RE = r"(?P<lang>\b(?!po\b)[-_@\w]+)"
FBASE_RE = r"(?P<filebase>[^/]+)" # No slashes or dots.
# List of regex to match. These should include a %(lang)s where the
# language locale should appear.
RE_LIST = (
    #^el.po Notice the ^, only matching in beginning.
    r"^%(lang)s\.po$",
    #^po/el.po: Notice the ^, only matching in beginning.
    r"^po/%(lang)s\.po$",
    #.../po/el.po: Too generic to avoid the po/ prefix.
    r".+/po/%(lang)s\.po$",
    #.../el/LC_MESSAGES/foo.po
    r".+/%(lang)s/LC_MESSAGES/%(fbase)s\.po$",
    #.../po/el/foo.po
    r".+/%(lang)s/%(fbase)s\.po$",
    #.../po/foo.el.po
    r".+/%(fbase)s\.%(lang)s\.po$",
    #^po-.../el.po: Intltool multi-domain support (multiple sub-projects)
    r"^po-.+/%(lang)s\.po$",
)
# Inject the language regex into the list elements
RE_LIST = [re.compile(r % {'lang': LANG_RE, 'fbase': FBASE_RE})
                      for r in RE_LIST]

def run_msgfmt_check(po_contents, with_exceptions=True):
    """
    Run a `msgfmt -c` on a file (file object).

    Return the output of the execution of the command.
    """
    command = 'msgfmt -o /dev/null -c -'
    status, stdout, stderr = run_command(command, _input=po_contents,
        with_extended_output=True, with_exceptions=with_exceptions)
    # Not sure why msgfmt sends its output to stderr instead of stdout
    return {'status': status,
            'stdout': stdout,
            'stderr' : stderr,}

class POTStatsError(Exception):

    def __init__(self, language):
        self.language = language

    def __str__(self):
        return ("Could not calculate the statistics using the '%s' "
               "language." % (self.language))

class FileFilterError(Exception):

    def __str__(self):
        return ("The file filter should allows the POTFILES.in file"
               " for intltool POT-based projects.")

class MsgfmtCheckError(Exception):

    def __str__(self):
        return "Msgfmt -c check failed for the file."

class SourceFileError(Exception):

    def __str__(self):
        return repr("No POT file found.")

class POTManager(TransManagerMixin):
    """
    A browser class for Managing POT files.

    Parameter:
    full_name: Name used for identifying set of msgmerged files related to POT/PO
               files found in `path`.
    path: Diretiry base where the POT/PO files can be found.
    source_language: The code of the source language. Usually it's English (en).
    file_filter: Regex for find the POT/PO under `path`.

    """

    def __init__(self, full_name, path, source_lang, file_filter):
        self.full_name = full_name
        self.path = path
        self.source_lang = source_lang
        self.file_filter = file_filter
        # Static directory
        self.msgmerge_path = os.path.join(settings.MSGMERGE_DIR, full_name)

    def guess_language(self, filename):
        """Guess a language from the filename.
        
        A number of regexxes will be applied, and the first one which matches
        is the winner.
        """

        for regex in RE_LIST:
            m = regex.match(filename)
            if m:
                return m.group('lang')

    def guess_po_dir(self):
        """Guess the po/ diretory to run intltool."""
        for filename in self.get_files(self.file_filter):
            # FIXME: It seems intltool-based projects can survive without a
            # POTFILES.in file. It must identify it in another way.
            if 'POTFILES.in' in filename:
                if self.file_filter:
                    if re.compile(self.file_filter).match(filename):
                        return os.path.join(self.path, 
                                      os.path.dirname(filename))
        raise FileFilterError, ("File filter does not allow 'POTFILES.in' file"
                                " or it does not exist in the file system.")

    def get_po_files(self):
        """Return a list of PO filenames."""
        for filename in self.get_files(self.file_filter):
            if filename.endswith('.po'):
                yield filename

    def get_lang_files(self, lang):
        """Return a list with the PO filenames for a specificy language."""
        for filename in self.get_po_files():
            if self.guess_language(filename) == lang:
                yield filename

    def get_langs(self):
        """Return all langs tha have a po file for a object."""
        langs = []
        for filename in self.get_po_files():
            lang_code = self.guess_language(filename)
            if lang_code not in langs:
                langs.append(lang_code)
                yield lang_code

    def get_file_path(self, filename, is_msgmerged=False):
        """
        Return the full path of the filename.

        If `is_msgmerged` is set to True the path of the merged file is returned.

        """
        if is_msgmerged:
            file_path = os.path.join(self.msgmerge_path, filename)
        else:
            file_path = os.path.join(self.path, filename)

        if not os.path.exists(file_path):
            raise IOError, "File '%s' does not exist." % file_path
 
        return file_path

    def get_file_contents(self, filename, is_msgmerged=False, decode=None):
        """
        Return the file contents of the requested file.

        If `is_msgmerged` is set to True the merged file stored is opened.
        If `decode` is specified the contents are decoded with the
        `decode` encoding.

        """
        file_path = self.get_file_path(filename, is_msgmerged)
        fp = file(file_path, 'rb')
        try:
            content = fp.read()
        finally:
            fp.close()

        if decode:
            content = content.decode(decode)
        return content

    def get_po_entries(self, filename):
        """Return a polib.POFile object with the entries from filename."""
        file_path = self.get_file_path(filename, True)
        return polib.pofile(file_path)


    def get_source_files(self):
        """
        Return a list with the source files (pot) paths 

        Try to find it in the file_set passed to the PO file instace. 
        If it still fails, try to find the POT file in the filesystem.
        """
        pofiles=[]
        for filename in self.get_files(self.file_filter):
            if filename.endswith('.pot'):
                pofiles.append(filename)

        # If there is no POT in the default path, try to find it in msgmerged one
        if not pofiles:
            for filename in self.get_files(self.file_filter, self.msgmerge_path):
                if filename.endswith('.pot'):
                    pofiles.append(filename)
        return pofiles


    def get_source_file_for_pofile(self, filename):
        """
        Find the related source file (POT) for a pofile when it has multiple
        source files.

        This method gets a filename as parameter and tries to discover the 
        related POT file using two methods:
        
        1. Trying to find a POT file with the same base path that the pofile.
           Example: /foo/bar.pot and /foo/baz.po match on this method.

        2. Trying to find a POT file with the same domain that the pofile in any
           directory.
        
           Example: /foo/bar.pot and /foo/baz/bar.po match on this method.
           The domain in this case is 'bar'.

        If no POT is found the method returns None.
        
        """
        # For filename='/foo/bar.po'
        fb = os.path.basename(filename) # 'bar.po'
        fp = filename.split(fb)[0]        # '/foo/'

        source_files = self.get_source_files()

        # Find the POT with the same domain or path that the filename,
        # if the component has more that one POT file
        if len(source_files) > 1:
            for source in source_files:
                sb = os.path.basename(source)
                if sb.endswith('.pot'):
                    sb = sb[:-1]
                pb = source.split(sb)[0]
                if pb==fp or sb==fb:
                    return source
        elif len(source_files) == 1:
            return source_files[0]
        else:
            return None

    @staticmethod
    def get_po_stats(po_contents):
        """
        Return a dictionary with the stats for a POT/PO file content.

        Case the stats for the ``pofile`` can not be calculated, the dictionary
        will be returned with stats equals zero and with the ``error`` attribute
        set as True.

        """
        error = False
        output = ''
        try:
            # These env vars are needed to ensure the command output be in English
            env = {'LC_ALL':'C', 'LANG':'C', 'LANGUAGE':'C'}
            command = "msgfmt --statistics -o /dev/null -"
            status, stdout, stderr = run_command(command, env=env, 
                _input=po_contents, with_extended_output=True)
            # Not sure why msgfmt sends its output to stderr instead of stdout
            output = stderr
        except CommandError, e:
            error = True
            logger.debug("'msgfmt --statistics' FAILED: %s" % str(e))

        r_tr = re.search(r"([0-9]+) translated", output)
        r_un = re.search(r"([0-9]+) untranslated", output)
        r_fz = re.search(r"([0-9]+) fuzzy", output)

        if r_tr: translated = r_tr.group(1)
        else: translated = 0
        if r_un: untranslated = r_un.group(1)
        else: untranslated = 0
        if r_fz: fuzzy = r_fz.group(1)
        else: fuzzy = 0

        return {'translated' : int(translated),
                'fuzzy' : int(fuzzy),
                'untranslated' : int(untranslated),
                'error' : error,}

    @staticmethod
    def get_stats_completion(stats):
        """
        Get a dictionary with the translation stats of a pofile and returns the 
        completion of it.

        The ``stats`` parameter must receive a dictionary like the following:
        stats = {'translated': 50, 'fuzzy': 20, 'untranslated': 30}
        """
        try:
            total = (stats.get('translated') + stats.get('fuzzy') + stats.get('untranslated'))
            return (stats.get('translated') * 100 / total)
        except ZeroDivisionError:
            pass
        return None

    @staticmethod
    def get_stats_status(stats):
        """
        Get a dictionary with the translation stats of a pofile and returns a 
        string with the status in the following format:
        '10 messages complete with 1 fuzzy and 12 untranslated'

        The ``stats`` parameter must receive a dictionary like the following:
        stats = {'translated': 50, 'fuzzy': 20, 'untranslated': 30}
        """
        from django.template.defaultfilters import pluralize
        status = "%s message%s complete with %s fuzz%s and %s untranslated" \
            % (stats['translated'], pluralize(stats['translated']),
               stats['fuzzy'], pluralize(stats['fuzzy'], 'y,ies'),
               stats['untranslated'])
        return status

    def calculate_file_stats(self, filename, source_file, try_to_merge):
        """
        Return the stats of a specificy file copying it to the static directory.

        If `try_to_merge` is set to True, the stats are calculated after merging
        the PO file with the related POT.
        """
        if try_to_merge:
            # Only try to get the POT for a PO when it's really needed.
            # It might be an expensive operation
            if not source_file:
                is_msgmerged = False
                logger.debug("No POT file found for the '%s' file." % filename)
            else:
                is_msgmerged = self.msgmerge(filename, source_file)
        else:
            is_msgmerged = False

        #Copy the current file (non-msgmerged) to the static dir
        if not is_msgmerged:
            logger.debug("Copied original file (non-msgmerged) to the cache "
                "dir.")
            self.copy_file_to_static_dir(filename)

        po_contents = self.get_file_contents(filename, is_msgmerged)
        postats = self.get_po_stats(po_contents)

        result = {'trans': postats['translated'],
                  'fuzzy': postats['fuzzy'],
                  'untrans': postats['untranslated'],
                  'error': postats['error'],
                  'is_msgmerged': is_msgmerged}
        logger.debug("Stats: %s" % result)
        return result

    @staticmethod
    def msgfmt_check(po_contents):
        """
        Call run_msgfmt_check (runs a `msgfmt -c` on a file (file object)).

        Raise a MsgfmtCheckError in case the stderror has errors or warnings or
        the command execution returns Error.
        """
        
        try:
            command = 'msgfmt -o /dev/null -c -'
            status, stdout, stderr = run_msgfmt_check(po_contents)
            # Not sure why msgfmt sends its output to stderr instead of stdout
            if 'warning:' in stderr or 'too many errors, aborting' in stderr:
                raise CommandError(command, status, stderr)
        except CommandError:
            raise MsgfmtCheckError, ("Your file does not pass by the check "
                "for correctness (msgfmt -c). Please run this command on "
                "your system to see the errors.")

    def msgmerge(self, pofile, potfile):
        """
        Merge two files and save the output at the static diretory.

        In case of error, copy the file (pofile) to the destination without 
        merging it.

        """
        is_msgmerged = True
        outpo = os.path.join(self.msgmerge_path, pofile)
        
        #Create dir for the static file
        msgmerge_dir = os.path.dirname(outpo)
        if not os.path.exists(msgmerge_dir):
            os.makedirs(msgmerge_dir)

        logger.debug("Trying to merge the PO '%s' with POT '%s'." % (pofile,
            potfile))

        try:
            # TODO: Find a library to avoid call msgmerge by command
            command = "msgmerge -o %(outpo)s %(pofile)s %(potfile)s" % {
                      'outpo': outpo,
                      'pofile': os.path.join(self.path, pofile),
                      'potfile': os.path.join(self.msgmerge_path, potfile),}
            stdout = run_command(command)
        except CommandError, e:
            is_msgmerged = False
            logger.debug("MSGMERGE FAILED: %s" % str(e))
        return is_msgmerged

    def intltool_update(self):
        """
        Create a new POT file using "intltool-update -p" from the 
        source files. Return False if it fails.
        """
        po_dir = self.guess_po_dir()
        error = False
        try:
            stdout = run_command("rm -f missing notexist", cwd=po_dir)
            stdout = run_command("intltool-update -p", cwd=po_dir)
        except CommandError, e:
            error = True
            logger.debug("INTLTOOL FAILED: %s" % str(e))

        # Copy the potfile if it exist to the merged files directory
        potfiles = self.get_source_files()
        for potfile in potfiles:
            self.copy_file_to_static_dir(potfile)

        if error:
            # TODO: Log this. output var can be used.
            return False

        return True

    def copy_file_to_static_dir(self, filename):
        """Copy a file to the statc msgmerge directory."""
        import shutil
        dest = os.path.join(self.msgmerge_path, filename)

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        shutil.copyfile(os.path.join(self.path, filename), dest)

    def delete_file_from_static_dir(self, filename):
        """Delete a file from the static cache dir"""
        dest = os.path.join(self.msgmerge_path, filename)
        try:
            os.remove(dest)
        except OSError:
            pass
