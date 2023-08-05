from testtools import TestCase

import mocker


class TestCaseWithMocker(TestCase):

    def setUp(self):
        super(TestCaseWithMocker, self).setUp()
        self.mocker = mocker.Mocker()

    def tearDown(self):
        self.mocker.restore()
        self.mocker.verify()
        super(TestCaseWithMocker, self).tearDown()
