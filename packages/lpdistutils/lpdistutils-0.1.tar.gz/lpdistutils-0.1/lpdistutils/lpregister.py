import os
import string
import sys
import time

from distutils import log

from launchpadlib.errors import HTTPError

from bzrlib import errors, transport
from bzrlib.branch import Branch
from bzrlib.plugins.launchpad import account

from lpdistutils import LPCommand


class NameAlreadyExists(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s already exists" % self.name


class Register(object):

    def __init__(self, launchpad):
        self.launchpad = launchpad

    def register(self, metadata):
        name = metadata.name
        try:
            self.launchpad.projects[name].name
            raise NameAlreadyExists(name)
        except KeyError:
            pass
        except HTTPError, e:
            if e.response.status != "404":
                raise
            pass
        project = self.launchpad.projects.new_project(
            description=metadata.long_description,
            display_name=name,
            home_page_url=metadata.url,
            # FIXME: go from metadata.get_license() to acceptable values for
            # this
            licenses=None,
            name=name,
            programming_lang="Python",
            # FIXME: something else for the summary would be nice
            summary=metadata.description,
            title=metadata.description,
            )
        return project


class lpregister(LPCommand):

    description = ("register the project with the Launchpad.")
    user_options = LPCommand.user_options + []
    boolean_options = LPCommand.boolean_options + []

    def initialize_options(self):
        LPCommand.initialize_options(self)

    def finalize_options(self):
        LPCommand.finalize_options(self)

    def run(self):
        self.finalize_options()
        self.check_metadata()
        lp = self.get_lp()
        project = self.send_metadata(lp)
        self.write_lpinfo(project)
        self.push_bzr(lp, project)

    def check_metadata(self):
        """Ensure that all required elements of meta-data (name, version,
           URL, (author and author_email) or (maintainer and
           maintainer_email)) are supplied by the Distribution object; warn if
           any are missing.
        """
        metadata = self.distribution.metadata

        missing = []
        for attr in ('name', 'description'):
            if not (hasattr(metadata, attr) and getattr(metadata, attr)):
                missing.append(attr)

        if missing:
            raise ValueError("missing required meta-data: " +
                      string.join(missing, ", "))

    def send_metadata(self, lp):
        ''' Send the metadata to the package index server.'''
        meta = self.distribution.metadata
        register = Register(lp)
        project = register.register(meta)
        self.announce('Project created!', log.INFO)
        return project

    def write_lpinfo(self, project):
        lpinfo = self.get_lpinfo()
        lpinfo.set_name(project.name)
        lpinfo.save()

    def push_bzr(self, lp, project):
        basedir = os.path.dirname(sys.argv[0])
        if basedir == '':
            basedir = '.'
        try:
            branch = Branch.open_containing(basedir)[0]
        except errors.NotBranchError:
            return
        username = account.get_lp_login()
        if username is None:
            return
        url = 'lp:~%s/%s/trunk' % (username, self.distribution.metadata.name)
        to_transport = transport.get_transport(url)
        br_to = branch.create_clone_on_transport(to_transport)
        branch.set_push_location(br_to.base)
        self.announce('Branch pushed, sleeping to wait for LP to scan it.',
                log.INFO)
        time.sleep(60)
        self.set_trunk_branch(lp, project, url)

    def set_trunk_branch(self, lp, project, url):
        series = project.series[0]
        branch = lp.branches.getByUrl(url=url)
        series.branch = branch
        series.lp_save()
