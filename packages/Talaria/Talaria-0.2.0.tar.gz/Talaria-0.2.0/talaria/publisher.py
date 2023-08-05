# -*- coding: utf-8 -*-
import os
from mercurial import ui, hg, util

from talaria.repo import Repo
from talaria.pages import BasePage
from talaria.graph import accessibility


class Publisher(object):
    """
    Web site publisher.
    """

    def __init__(self, hgrepo):
        self.hg = hgrepo
        self.www_dir = self.hg.ui.config(
                'talaria', 'www', 'www').rstrip()
        self.revision_file = self.hg.ui.config(
                'talaria', 'revision_file', '.hgrevision')

    def published_revision(self):
        """ Return published revision"""
        revision_file = os.path.join(self.www_dir, self.revision_file)
        if os.path.isfile(revision_file):
            fd = open(revision_file)
            revision = fd.read().strip()
            fd.close()
        else:
            revision = 'null'
        return self.hg[revision]

    def get_changes(self, rev1, rev2):
        """ Return tuple of changed files between two revisions:

        @param node1: is a first (start) node
        @param node2: is a second one
        @return: tuple with lists containing modified, added and removed files
        """
        modified, added, removed, _, _, _, _ = self.hg.status(rev1, rev2)
        return modified, added, removed

    def has_local_changes(self):
        modified, added, removed, _, _, _, _ = self.hg.status('tip', None)
        return bool(modified or added or removed)

    def amend(self):
        """ Amend last commit by inserting local changes into

        Method rolls to one commit back, then update current commit, then
        perform new publishing again
        """
        if not hasattr(self.hg, 'mq'):
            raise util.Abort('MQ extension is not plugged in')
        rev2 = self.hg['tip'].parents()[0]
        mq = self.hg.mq
        self.publish(rev2)
        mq.qimport(self.hg, files=[], patchname='talaria-amend', rev=['tip'],
                git=True)
        mq.refresh(self.hg)
        mq.finish(self.hg, ['tip'])
        self.publish()

    def _publish_static(self, repo1, repo2):
        # remove everything which is old
        for repoitem, outitem in repo1.media.iteritems():
            if repo2.hgpath.isdir(repoitem):
                repodir_ = repoitem + '/'
                mediafiles = [
                    f for f in repo1.hgpath.files if f.startswith(repodir_)
                ]
                mediadirs = [
                   d for d in repo1.hgpath.directories \
                            if d.startswith(repodir_)
                ]
                mediadirs.append(repoitem)
                for filename in mediafiles:
                    outfile = os.path.join(
                        repo1.www_dir, outitem, filename[len(repodir_):]
                    )
                    if os.path.isfile(outfile):
                        os.unlink(outfile)
                for dirname in mediadirs:
                    outdir = os.path.join(
                        repo1.www_dir, outitem, dirname[len(repodir_):]
                    )
                    if os.path.isdir(outdir) and not os.listdir(outdir):
                        os.rmdir(outdir)
            elif repo2.hgpath.isfile(repoitem):
                outfile = os.path.join(repo1.www_dir, outitem)
                if os.path.isfile(outfile):
                    os.unlink(outfile)
        # create everything which is new and fresh
        for repoitem, outitem in repo2.media.iteritems():
            if repo2.hgpath.isdir(repoitem):
                repodir_ = repoitem + '/'
                mediafiles = [
                    f for f in repo2.hgpath.files if f.startswith(repodir_)
                ]
                mediadirs = [
                   d for d in repo2.hgpath.directories \
                            if d.startswith(repodir_)
                ]
                mediadirs.append(repoitem)
                for dirname in mediadirs:
                    outdir = os.path.join(
                        repo2.www_dir, outitem, dirname[len(repodir_):]
                    )
                    try: os.makedirs(outdir)
                    except OSError: pass
                for filename in mediafiles:
                    outfile = os.path.join(
                        repo2.www_dir, outitem, filename[len(repodir_):]
                    )
                    fd = open(outfile, 'w')
                    fd.write(repo2.hgpath.data(filename))
                    fd.close()
            elif repo2.hgpath.isfile(repoitem):
                outfile = os.path.join(repo1.www_dir, outitem)
                fd = open(outfile, 'w')
                fd.write(repo2.hgpath.data(repoitem))
                fd.close()


    def publish(self, rev2=None):
        """Publish website to a given revision

        Perform publishing to a given revision. Method defines current already
        published revision, finds a set of differences between revisions,
        builds the dependency tree and updates all changed pages.

        If rev2 isn't set, then "tip" is used
        """
        rev1 = self.published_revision()
        if rev2 is None:
            rev2 = self.hg['tip']
        modified, added, removed = self.get_changes(rev1, rev2)
        changed = modified + added + removed
        if not changed:
            return
        # remove pages from repo1
        repo1 = Repo(self.hg, rev1.hex())
        repo1.build_dependency_tree()
        tree1 = accessibility(repo1.dependency_tree)
        del_pages = set()
        for changed_file in changed:
            dependencies = tree1.get(changed_file, [])
            for item in dependencies:
                if isinstance(item, BasePage):
                    del_pages.add(item)
        # add pages to repo2
        repo2 = Repo(self.hg, rev2.hex())
        repo2.build_dependency_tree()
        tree2 = accessibility(repo2.dependency_tree)
        save_pages = set()
        for changed_file in changed:
            dependencies = tree2.get(changed_file, [])
            for item in dependencies:
                if isinstance(item, BasePage):
                    save_pages.add(item)
        # perform modifications
        for page in del_pages:
            page.delete()
        for page in save_pages:
            page.save()
        # publish static
        self._publish_static(repo1, repo2)
        # update revision file
        revision_file = os.path.join(self.www_dir, self.revision_file)
        fd = open(revision_file, 'w')
        fd.write('%s\n' % rev2.hex())
        fd.close()
