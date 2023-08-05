import os
import shutil
import sys
import tempfile

from testtools import TestCase

from distutils.dist import Distribution

from lpdistutils import LPCommand, LPInfo
from lpdistutils.tests import TestCaseWithMocker


class TestCaseInTempDir(TestCase):

    def setUp(self):
        super(TestCaseInTempDir, self).setUp()
        self.base_dir = tempfile.mkdtemp(prefix="lpdistutils-tests")
        self.addCleanup(shutil.rmtree, self.base_dir)


class LPInfoTests(TestCaseInTempDir):

    def get_nonexistant_filename(self):
        return os.path.join(self.base_dir, "nonexistant")

    def get_lpinfo_nonexistant_file(self):
        return LPInfo(self.get_nonexistant_filename())

    def test_set_name(self):
        lpinfo = self.get_lpinfo_nonexistant_file()
        lpinfo.set_name("foo")
        self.assertEqual(
            "foo", lpinfo.config.get(LPInfo.SECTION_NAME, "name"))

    def test_get_name(self):
        lpinfo = self.get_lpinfo_nonexistant_file()
        self.assertEqual(None, lpinfo.get_name())

    def test_get_name_after_set(self):
        lpinfo = self.get_lpinfo_nonexistant_file()
        lpinfo.set_name("foo")
        self.assertEqual("foo", lpinfo.get_name())

    def test_save(self):
        lpinfo = self.get_lpinfo_nonexistant_file()
        lpinfo.set_name("foo")
        lpinfo.save()
        self.assertTrue(os.path.exists(lpinfo.path))

    def test_save_and_load(self):
        path = self.get_nonexistant_filename()
        lpinfo = LPInfo(path)
        lpinfo.set_name("foo")
        lpinfo.save()
        new_lpinfo = LPInfo(path)
        self.assertEqual("foo", new_lpinfo.get_name())


class LPCommandTests(TestCaseWithMocker):

    def test_default_lpinstance(self):
        obj = self.mocker.replace('launchpadlib.launchpad.Launchpad')
        lp = self.mocker.mock()
        obj.login_with
        self.mocker.result(lp)
        result = object()
        lp(
            "lpdistutils", service_root="production",
            allow_access_levels=["WRITE_PUBLIC"])
        self.mocker.result(result)
        self.mocker.replay()
        dist = Distribution()
        cmd = LPCommand(dist)
        cmd.finalize_options()
        self.assertEqual(result, cmd.get_lp())

    def test_custom_lpinstance(self):
        obj = self.mocker.replace('launchpadlib.launchpad.Launchpad')
        lp = self.mocker.mock()
        obj.login_with
        self.mocker.result(lp)
        result = object()
        lp(
            "lpdistutils", service_root="staging",
            allow_access_levels=["WRITE_PUBLIC"])
        self.mocker.result(result)
        self.mocker.replay()
        dist = Distribution()
        cmd = LPCommand(dist)
        cmd.lpinstance = "staging"
        cmd.finalize_options()
        self.assertEqual(result, cmd.get_lp())

    def test_getlpinfo_same_dir(self):
        dist = Distribution()
        cmd = LPCommand(dist)
        cmd.finalize_options()
        sys.argv = ['setup.py', 'blah']
        self.assertEqual(".lpinfo", cmd.get_lpinfo().path)

    def test_getlpinfo_parent_dir(self):
        dist = Distribution()
        cmd = LPCommand(dist)
        cmd.finalize_options()
        sys.argv = ['../setup.py', 'blah']
        self.assertEqual("../.lpinfo", cmd.get_lpinfo().path)
