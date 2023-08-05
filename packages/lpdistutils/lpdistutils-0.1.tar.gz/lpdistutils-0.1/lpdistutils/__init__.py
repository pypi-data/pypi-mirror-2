import os
import sys

from distutils.cmd import Command

import ConfigParser

from launchpadlib.launchpad import Launchpad


class LPInfo(object):

    SECTION_NAME = "LAUNCHPAD"

    def __init__(self, path):
        self.path = path
        self.config = ConfigParser.SafeConfigParser()
        self.config.add_section(self.SECTION_NAME)
        self.config.read(self.path)

    def set_name(self, name):
        self.config.set(self.SECTION_NAME, "name", name)

    def get_name(self):
        if not self.config.has_option(self.SECTION_NAME, "name"):
            return None
        return self.config.get(self.SECTION_NAME, "name")

    def save(self):
        dirname = os.path.dirname(self.path)
        if dirname != '' and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.path, 'wb') as f:
            self.config.write(f)


class LPCommand(Command):

    DEFAULT_LPINSTANCE = "production"
    LPINFO_FILENAME = ".lpinfo"

    user_options = [
        ('lpinstance=', None,
         'which launchpad instance to use [default: %s]'
         % DEFAULT_LPINSTANCE),
        ]
    boolean_options = []

    def initialize_options(self):
        self.lpinstance = None

    def finalize_options(self):
        if self.lpinstance is None:
            self.lpinstance = self.DEFAULT_LPINSTANCE

    def get_lp(self):
        return Launchpad.login_with(
            "lpdistutils", service_root=self.lpinstance,
            allow_access_levels=["WRITE_PUBLIC"])

    def get_lpinfo(self):
        path = os.path.join(
            os.path.dirname(sys.argv[0]), self.LPINFO_FILENAME)
        return LPInfo(path)
