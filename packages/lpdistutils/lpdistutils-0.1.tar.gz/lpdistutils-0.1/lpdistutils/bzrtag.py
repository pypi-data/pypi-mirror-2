from distutils.cmd import Command
import os
import sys

from bzrlib.workingtree import WorkingTree


class UncommittedChanges(Exception):

    def __str__(self):
        return "There are uncommitted changes in the tree."


class TagAlreadyPresent(Exception):

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return "Tag %s is already present" % self.tag


class bzrtag(Command):

    description = ("Set a bzr tag based on the version.")
    user_options = [('force', 'f',
            'Force setting the tag, even if one is there or there '
            'are uncommitted changes')]
    boolean_options = []

    def initialize_options(self):
        self.force = False

    def finalize_options(self):
        pass

    def run(self):
        self.finalize_options()
        self.check_metadata()
        tree = self.get_tree()
        tree.lock_write()
        try:
            self.check_uncommited(tree)
            self.check_present(tree)
            self.set_tag(tree)
        finally:
            tree.unlock()

    def check_metadata(self):
        if getattr(self.distribution.metadata, "version", None) is None:
            raise AssertionError("You must specify version in setup.py")

    def get_tree(self):
        base = os.path.dirname(sys.argv[0])
        if base == '':
            base = '.'
        return WorkingTree.open_containing(base)[0]

    def check_uncommited(self, tree):
        if tree.changes_from(tree.basis_tree()).has_changed():
            if self.force:
                self.warn("Uncommitted changes.")
            raise UncommittedChanges

    def check_present(self, tree):
        if tree.branch.tags.has_tag(self.distribution.metadata.version):
            if self.force:
                self.warn("Tag already present.")
            raise TagAlreadyPresent

    def set_tag(self, tree):
        tree.branch.tags.set_tag(self.distribution.metadata.version,
                tree.branch.last_revision())
