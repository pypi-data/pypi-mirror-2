from distutils.dist import Distribution, DistributionMetadata

from testtools import TestCase

import mocker

from launchpadlib.errors import HTTPError

from lpdistutils.lpregister import (
    NameAlreadyExists,
    lpregister,
    Register,
    )
from lpdistutils.tests import TestCaseWithMocker


class NameAlreadyExistsTests(TestCase):

    def test_str(self):
        err = NameAlreadyExists("foo")
        self.assertEqual("foo already exists", str(err))


class RegisterTests(TestCaseWithMocker):

    def test_existing_project(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.mocker.mock()
        lp.projects[name].name
        self.mocker.result(self.mocker.mock())
        self.mocker.replay()
        register = Register(lp)
        self.assertRaises(NameAlreadyExists, register.register, metadata)

    def test_existing_project_500(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.mocker.mock()
        lp.projects[name].name
        resp = self.mocker.mock()
        e = HTTPError(resp, "")
        self.mocker.throw(e)
        resp.status
        self.mocker.result("500")
        self.mocker.replay()
        register = Register(lp)
        thrown = self.assertRaises(HTTPError, register.register, metadata)
        self.assertEqual(resp, thrown.response)

    def test_calls_new_project_on_KeyError(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.mocker.mock()
        lp.projects[name]
        self.mocker.throw(KeyError)
        lp.projects.new_project(mocker.KWARGS)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_calls_new_project_on_404(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.mocker.mock()
        lp.projects[name]
        resp = self.mocker.mock()
        self.mocker.throw(HTTPError(resp, ""))
        resp.status
        self.mocker.result("404")
        lp.projects.new_project(mocker.KWARGS)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def get_lp_with_new_project_args(self, metadata_name, **kwargs):
        lp = self.mocker.mock()
        lp.projects[metadata_name]
        self.mocker.throw(KeyError)
        lp.projects.new_project(mocker.KWARGS, **kwargs)
        return lp

    def test_new_project_call_contains_correct_name(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, name=name)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_contains_correct_display_name(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, display_name=name)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_unknown_url(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, home_page_url=None)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_known_url(self):
        metadata = DistributionMetadata()
        name = "foo"
        url = "http://example.com/foo"
        metadata.name = name
        metadata.url = url
        lp = self.get_lp_with_new_project_args(name, home_page_url=url)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_unknown_description(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, description=None)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_known_description(self):
        metadata = DistributionMetadata()
        name = "foo"
        long_description = "Long description"
        metadata.name = name
        metadata.long_description = long_description
        lp = self.get_lp_with_new_project_args(
            name, description=long_description)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_doesnt_pass_licenses(self):
        # We don't know how to translate the license field, but we
        # should fix that
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        metadata.license = "GPL"
        lp = self.get_lp_with_new_project_args(name, licenses=None)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_passes_programming_lang(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(
            name, programming_lang="Python")
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_unknown_summary(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, summary=None)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_known_summary(self):
        metadata = DistributionMetadata()
        name = "foo"
        description = "description"
        metadata.name = name
        metadata.description = description
        lp = self.get_lp_with_new_project_args(name, summary=description)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_unknown_title(self):
        metadata = DistributionMetadata()
        name = "foo"
        metadata.name = name
        lp = self.get_lp_with_new_project_args(name, title=None)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)

    def test_new_project_call_with_known_title(self):
        metadata = DistributionMetadata()
        name = "foo"
        description = "description"
        metadata.name = name
        metadata.description = description
        lp = self.get_lp_with_new_project_args(name, title=description)
        self.mocker.replay()
        register = Register(lp)
        register.register(metadata)


class lpregisterTests(TestCaseWithMocker):

    def setUp(self):
        super(lpregisterTests, self).setUp()
        self.REQUIRED_VALUES = ["name", "description"]

    def check_metadata(self, dist, expected):
        cmd = lpregister(dist)
        err = self.assertRaises(ValueError, cmd.run)
        self.assertEqual(
            "missing required meta-data: %s" % (", ".join(expected)),
            str(err))

    def test_check_metadata_no_name(self):
        dist = Distribution()
        self.check_metadata(dist, self.REQUIRED_VALUES)

    def test_check_metadata_with_name(self):
        dist = Distribution(attrs=dict(name="foo"))
        self.REQUIRED_VALUES.remove("name")
        self.check_metadata(dist, self.REQUIRED_VALUES)

    def test_check_metadata_no_description(self):
        dist = Distribution()
        self.check_metadata(dist, self.REQUIRED_VALUES)

    def test_check_metadata_with_description(self):
        dist = Distribution(attrs=dict(description="description"))
        self.REQUIRED_VALUES.remove("description")
        self.check_metadata(dist, self.REQUIRED_VALUES)

    def mock_launchpad(self):
        obj = self.mocker.replace('launchpadlib.launchpad.Launchpad')
        lp = self.mocker.mock()
        obj.login_with
        self.mocker.result(lp)
        lp(
            "lpdistutils", service_root="production",
            allow_access_levels=["WRITE_PUBLIC"])
        self.mocker.result(lp)
        return lp

    def test_send_metadata_calls_register(self):
        name = "foo"
        description = "description"
        dist = Distribution(attrs=dict(name=name, description=description))
        register = self.mocker.mock()
        lp = self.mock_launchpad()
        obj = self.mocker.replace('lpdistutils.lpregister.Register')
        obj(lp)
        self.mocker.result(register)
        register.register(dist.metadata)
        self.mocker.replay()
        cmd = lpregister(dist)
        cmd.finalize_options()
        cmd.send_metadata()

    def test_write_lpinfo_writes_lpinfo(self):
        name = "foo"
        dist = Distribution(attrs=dict(name=name))
        cmd = lpregister(dist)
        cmd.finalize_options()
        cls = self.mocker.replace('lpdistutils.LPInfo')
        obj = self.mocker.mock()
        cls(mocker.ANY)
        self.mocker.result(obj)
        obj.set_name(name)
        obj.save()
        self.mocker.replay()
        cmd.write_lpinfo()
