import os
import traceback

from django.conf import settings
from codebases.lib import BrowserMixin, BrowserError
from vcs.lib import RepoError
from vcs.lib.exceptions import *
from vcs.lib.types import need_repo
from vcs.lib.support.git import repository, clone
from txcommon.commands import CommandError
from txcommon.log import logger

REPO_PATH = settings.REPO_PATHS['git']

class GitBrowser(BrowserMixin):
    """
    A browser class for Git repositories.

    Git homepage: http://git.or.cz/

    >>> b = GitBrowser(root='http://git.fedorahosted.org/git/elections.git',
    ... name='test-git', branch='master')
    >>> GitBrowser(root='foo', name='../..', branch='tip')
    Traceback (most recent call last):
      ...
    AssertionError: Unit checkout path outside of nominal repo checkout path.
    """
    def __init__(self, root, name=None, branch='master'):
        # If name isn't given, let's take the last part of the root
        # Eg. root = 'http://example.com/foo/baz' -> name='baz'
        if not name:
            name = root.split('/')[-1]

        self.root = root
        self.branch = branch

        self.path = os.path.normpath(os.path.join(REPO_PATH, name))
        self.path = os.path.abspath(self.path)
        #Test for possible directory traversal
        assert os.path.commonprefix(
            [self.path, REPO_PATH]) == REPO_PATH, (
            "Unit checkout path outside of nominal repo checkout path.")

    @property
    def remote_path(self):
        """Return remote path for cloning."""
        return str(self.root)


    def setup_repo(self):
        """
        Initialize repository for the first time.

        Commands used:
        git clone <remote_path> <self.path>
        if branch != master:
        git branch <branch> <remote_branch>
        git co <branch>
        """

        try:
            repo = clone(self.remote_path, self.path)

            # Non master branches need more work:
            if self.branch != u'master':
                remote_branch = 'origin/%s' % self.branch

                repo.branch(self.branch, remote_branch)
                repo.checkout(self.branch)

            self.repo = repo
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            self.teardown_repo()
            raise SetupRepoError(e)


    def init_repo(self):
        """
        Initialize the ``repo`` variable on the browser.

        If local repo exists, use that. If not, clone it.
        """
        try:
            self.repo = repository(self.path)
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise InitRepoError(e)

    def _clean_dir(self):
        """
        Clean the local working directory.

        Reset any pending changes.

        Commands used:
        git reset --hard
        """
        try:
            self.repo.reset('--hard')
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise CleanupRepoError(e)

    @need_repo
    def update(self):
        """
        Fully update the local repository.

        Commands used:
        git fetch origin
        git reset --hard <revspec>
        """
        try:
            revspec = 'origin/%s' % self.branch
            self.repo.fetch('origin')
            self.repo.reset(revspec, hard=True)
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise UpdateRepoError(e)

    @need_repo
    def get_rev(self, obj=None):
        """
        Get the current revision of the repository or a specific
        object.
        
        Commands used:
        git show-ref refs/heads/<branch>
        git log -1 --pretty=format:%H <obj>
        """
        try:
            if not obj:
                refspec = 'refs/heads/%s' % self.branch
                rev = self.repo.show_ref(refspec).split()[0]
            else:
                rev = self.repo.log('-1', '--pretty=format:%H', obj)
            if rev:
                return (int(rev, 16),)
            else:
                return (0,)
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise RevisionRepoError(e)

    @need_repo
    def submit(self, files, msg, user):
        """
        git add <filename>
        git commit -m <msg> --author=<user> <filename>
        """
        filenames = []
        for fieldname, uploadedfile in files.iteritems():
            filenames.append(uploadedfile.targetfile)
            self.save_file_contents(uploadedfile.targetfile,
                uploadedfile)

            self.repo.add(uploadedfile.targetfile)

        user = self._get_user(user).encode('utf-8')
        files = ' '.join(filenames).encode('utf-8')

        try:
            self.repo.commit(files, m=msg.encode('utf-8'), author=user)
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise CommitRepoError(e)

        try:
            self.repo.push('origin', self.branch)
        except Exception, e:
            if hasattr(e, 'stderr'):
                e = e.stderr
            raise PushRepoError(e)

