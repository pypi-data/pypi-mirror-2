import unittest
import os

from os.path import join, isdir

from jarn.mkrelease.scm import Mercurial

from jarn.mkrelease.process import Process

from jarn.mkrelease.testing import MercurialSetup
from jarn.mkrelease.testing import MockProcess
from jarn.mkrelease.testing import quiet


class ValidUrlTests(unittest.TestCase):

    def testSshUrl(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url('ssh://'), True)

    def testHttpUrl(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url('http://'), True)

    def testHttpsUrl(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url('https://'), True)

    def testFileUrl(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url('file://'), True)

    def testBadProtocol(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url('svn://'), False)

    def testEmptyString(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_url(''), False)


class ValidSandboxTests(MercurialSetup):

    def testSandbox(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_sandbox(self.packagedir), True)

    def testSubdirOfSandbox(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_sandbox(join(self.packagedir, 'testpackage')), True)

    def testNotExists(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_sandbox('foo'), False)

    def testNotADir(self):
        scm = Mercurial()
        self.assertEqual(scm.is_valid_sandbox(join(self.packagedir, 'setup.py')), False)

    def testNotACheckout(self):
        scm = Mercurial()
        self.destroy()
        self.assertEqual(scm.is_valid_sandbox(self.packagedir), False)

    @quiet
    def testCheckRaises(self):
        scm = Mercurial()
        self.assertRaises(SystemExit, scm.check_valid_sandbox, 'foo')
        self.assertRaises(SystemExit, scm.check_valid_sandbox, join(self.packagedir, 'setup.py'))
        self.destroy()
        self.assertRaises(SystemExit, scm.check_valid_sandbox, self.packagedir)


class BranchFromSandboxTests(MercurialSetup):

    def testGetLocalBranch(self):
        scm = Mercurial()
        self.assertEqual(scm.get_branch_from_sandbox(self.packagedir), 'default')

    def testGetLocalBranchFromBranch(self):
        scm = Mercurial()
        self.branch(self.packagedir, '2.x')
        self.assertEqual(scm.get_branch_from_sandbox(self.packagedir), '2.x')

    def testGetRemoteBranch(self):
        scm = Mercurial()
        self.clone()
        self.assertEqual(scm.get_branch_from_sandbox(self.clonedir), 'default')

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.get_branch_from_sandbox, self.packagedir)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.get_branch_from_sandbox, self.packagedir)


class UrlFromSandboxTests(MercurialSetup):

    def testGetLocalUrl(self):
        scm = Mercurial()
        self.assertEqual(scm.get_url_from_sandbox(self.packagedir), '')

    def testGetRemoteUrl(self):
        scm = Mercurial()
        self.clone()
        self.assertEqual(scm.get_url_from_sandbox(self.clonedir), self.packagedir)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.get_url_from_sandbox, self.packagedir)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.get_url_from_sandbox, self.packagedir)


class RemoteSandboxTests(MercurialSetup):

    def testIsLocal(self):
        scm = Mercurial()
        self.assertEqual(scm.is_remote_sandbox(self.packagedir), False)

    def testIsRemote(self):
        scm = Mercurial()
        self.clone()
        self.assertEqual(scm.is_remote_sandbox(self.clonedir), True)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.is_remote_sandbox, self.packagedir)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.is_remote_sandbox, self.packagedir)


class DirtySandboxTests(MercurialSetup):

    def testCleanSandbox(self):
        scm = Mercurial()
        self.assertEqual(scm.is_dirty_sandbox(self.packagedir), False)

    def testModifiedFile(self):
        scm = Mercurial()
        self.modify(self.packagedir)
        self.assertEqual(scm.is_dirty_sandbox(self.packagedir), True)

    def testRemovedFile(self):
        scm = Mercurial()
        self.remove(self.packagedir)
        self.assertEqual(scm.is_dirty_sandbox(self.packagedir), True)

    def testDeletedButTrackedFile(self):
        scm = Mercurial()
        self.delete(self.packagedir)
        # Note: The sandbox is reported as clean
        self.assertEqual(scm.is_dirty_sandbox(self.packagedir), False)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.is_dirty_sandbox, self.packagedir)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.is_dirty_sandbox, self.packagedir)

    @quiet
    def testCheckRaises(self):
        scm = Mercurial()
        self.modify(self.packagedir)
        self.assertRaises(SystemExit, scm.check_dirty_sandbox, self.packagedir)


class UncleanSandboxTests(DirtySandboxTests):

    def testCleanSandbox(self):
        scm = Mercurial()
        self.assertEqual(scm.is_unclean_sandbox(self.packagedir), False)

    def testModifiedFile(self):
        scm = Mercurial()
        self.modify(self.packagedir)
        self.assertEqual(scm.is_unclean_sandbox(self.packagedir), True)

    def testRemovedFile(self):
        scm = Mercurial()
        self.remove(self.packagedir)
        self.assertEqual(scm.is_unclean_sandbox(self.packagedir), True)

    def testDeletedButTrackedFile(self):
        scm = Mercurial()
        self.delete(self.packagedir)
        # Note: The sandbox is reported as unclean
        self.assertEqual(scm.is_unclean_sandbox(self.packagedir), True)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.is_unclean_sandbox, self.packagedir)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.is_unclean_sandbox, self.packagedir)

    @quiet
    def testCheckRaises(self):
        scm = Mercurial()
        self.modify(self.packagedir)
        self.assertRaises(SystemExit, scm.check_unclean_sandbox, self.packagedir)


class CheckinSandboxTests(MercurialSetup):

    def testCheckinCleanSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.assertEqual(scm.checkin_sandbox(self.packagedir, 'testpackage', '2.6', False), 0)

    def testCheckinDirtySandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.modify(self.packagedir)
        self.assertEqual(scm.checkin_sandbox(self.packagedir, 'testpackage', '2.6', False), 0)

    def testCheckinAndPushCleanLocalSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.assertEqual(scm.checkin_sandbox(self.packagedir, 'testpackage', '2.6', True), 0)

    def testCheckinAndPushDirtyLocalSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.modify(self.packagedir)
        self.assertEqual(scm.checkin_sandbox(self.packagedir, 'testpackage', '2.6', True), 0)

    def testCheckinAndPushCleanRemoteSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.clone()
        self.assertEqual(scm.checkin_sandbox(self.clonedir, 'testpackage', '2.6', True), 0)

    def testCheckinAndPushDirtyRemoteSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.clone()
        self.modify(self.clonedir)
        self.assertEqual(scm.checkin_sandbox(self.clonedir, 'testpackage', '2.6', True), 0)
        self.verify(self.clonedir)
        self.update(self.packagedir)
        self.verify(self.packagedir)

    @quiet
    def testBadPush(self):
        scm = Mercurial(Process(quiet=True))
        self.clone()
        self.destroy()
        self.assertRaises(SystemExit, scm.checkin_sandbox, self.clonedir, 'testpackage', '2.6', True)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.checkin_sandbox, self.packagedir, 'testpackage', '2.6', False)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.checkin_sandbox, self.packagedir, 'testpackage', '2.6', False)


class CheckoutUrlTests(MercurialSetup):

    def testCheckoutUrl(self):
        scm = Mercurial(Process(quiet=True))
        self.assertEqual(scm.checkout_url(self.packagedir, 'testclone'), 0)
        self.assertEqual(isdir('testclone'), True)

    @quiet
    def testBadServer(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.checkout_url, self.packagedir, 'testclone')

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.checkout_url, self.packagedir, 'testclone')


class TagExistsTests(MercurialSetup):

    def testTagDoesNotExist(self):
        scm = Mercurial()
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), False)

    def testTagExists(self):
        scm = Mercurial()
        self.tag(self.packagedir, '2.6')
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), True)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.check_tag_exists, self.packagedir, '2.6')

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.check_tag_exists, self.packagedir, '2.6')

    @quiet
    def testCheckRaises(self):
        scm = Mercurial()
        self.tag(self.packagedir, '2.6')
        self.assertRaises(SystemExit, scm.check_tag_exists, self.packagedir, '2.6')


class CreateTagTests(MercurialSetup):

    def testCreateTag(self):
        scm = Mercurial()
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), False)
        self.assertEqual(scm.create_tag(self.packagedir, '2.6', 'testpackage', '2.6', False), 0)
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), True)

    @quiet
    def testCreateExistingTag(self):
        scm = Mercurial(Process(quiet=True))
        self.assertEqual(scm.create_tag(self.packagedir, '2.6', 'testpackage', '2.6', False), 0)
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), True)
        self.assertRaises(SystemExit, scm.create_tag, self.packagedir, '2.6', 'testpackage', '2.6', False)

    def testCreateAndPushLocalTag(self):
        scm = Mercurial()
        self.assertEqual(scm.create_tag(self.packagedir, '2.6', 'testpackage', '2.6', True), 0)
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), True)

    def testCreateAndPushRemoteTag(self):
        scm = Mercurial(Process(quiet=True))
        self.clone()
        self.assertEqual(scm.create_tag(self.clonedir, '2.6', 'testpackage', '2.6', True), 0)
        self.assertEqual(scm.tag_exists(self.clonedir, '2.6'), True)
        self.assertEqual(scm.tag_exists(self.packagedir, '2.6'), True)

    @quiet
    def testBadPush(self):
        scm = Mercurial(Process(quiet=True))
        self.clone()
        self.destroy()
        self.assertRaises(SystemExit, scm.create_tag, self.packagedir, '2.6', 'testpackage', '2.6', True)

    @quiet
    def testBadSandbox(self):
        scm = Mercurial(Process(quiet=True))
        self.destroy()
        self.assertRaises(SystemExit, scm.create_tag, self.packagedir, '2.6', 'testpackage', '2.6', False)

    @quiet
    def testBadProcess(self):
        scm = Mercurial(MockProcess(rc=1))
        self.assertRaises(SystemExit, scm.create_tag, self.packagedir, '2.6', 'testpackage', '2.6', False)


class GetVersionTests(unittest.TestCase):

    def testGetVersion(self):
        scm = Mercurial()
        self.failIfEqual(scm.get_version(), None)

    def testVersionTuple(self):
        scm = Mercurial()
        self.failIfEqual(scm.version_tuple, ())

