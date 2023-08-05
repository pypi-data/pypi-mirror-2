from __future__ import with_statement

import os
import shutil
import unittest

import simplejson as ConfigModule

import cloudpool.shell as ShellModule

class TestSecureShell(unittest.TestCase):

    @staticmethod
    def loadCredentials():

        configFilePath = os.path.join(
            os.getcwd(), 'test', 'config')

        with open(configFilePath) as f:

            config = ConfigModule.load(f)

            remoteExecuteCredentials = config['remote execute credentials']
            assert len(remoteExecuteCredentials), 'expected to find remote execute credentials'

            return remoteExecuteCredentials

        raise NotImplemented(
            'could not read credentials from config file %s' % configFilePath)




    @staticmethod
    def getShell():

        shell = ShellModule.SecureShell()
        # set the hostname, user, and keyfile

        credentials = TestSecureShell1.loadCredentials()

        credential = credentials[0]

        hostname = credential['hostname']
        user = credential['user']
        keyfile = credential['keyfile']

        shell.hostname(hostname)
        shell.user(user)
        shell.keyfile(keyfile)

        return shell
    
    # END class TestSecureShell
    pass


class TestSecureShell1(TestSecureShell):

    STAGE_ROOT = ['', 'tmp']

    def setUp(self):
        self.shell = TestSecureShell.getShell()
        self.shell.stageRoot(TestSecureShell1.STAGE_ROOT)
        return

    def testConstructPaths(self):
        path = ['path', 'to', 'file']
        localpath, remotepath = self.shell.constructPaths(path)
        self.assertEquals(os.path.sep.join(path),
                          localpath)
        self.assertEquals(self.shell.getStagedPath(localpath),
                          remotepath)

        path = '/path/to/file'
        localpath, remotepath = self.shell.constructPaths(path)
        self.assertEquals(os.path.join(path),
                          localpath)
        self.assertEquals(self.shell.getStagedPath(localpath),
                          remotepath)

        return


    def testGetStagedPath(self):
        path = ['path', 'to', 'file']
        stagedPath = self.shell.getStagedPath(path)
        expected = os.path.sep.join(TestSecureShell1.STAGE_ROOT + path)
        self.assertEquals(
            expected,
            stagedPath)

        path = os.path.sep.join(path)
        stagedPath = self.shell.getStagedPath(path)
        self.assertEquals(
            expected,
            stagedPath)

        return

    # END class TestSecureShell1
    pass


class TestSecureShell2(TestSecureShell1):

    BASE_DIR = os.path.join(os.getcwd(), 'resources', 'testdata', 'TestShell')
    DATA_DIR = os.path.sep.join([BASE_DIR, 'dirToStage'])
    STAGING_LOCAL_DIR = os.path.sep.join(['', 'tmp', 'TestShell', 'dirToStage'])

    def setUp(self):
        TestSecureShell1.setUp(self)

        if os.path.exists(TestSecureShell2.STAGING_LOCAL_DIR):
            shutil.rmtree(TestSecureShell2.STAGING_LOCAL_DIR)

        shutil.copytree(TestSecureShell2.DATA_DIR,
                        TestSecureShell2.STAGING_LOCAL_DIR)
        pass

    def tearDown(self):
        if os.path.exists(TestSecureShell2.STAGING_LOCAL_DIR):
            shutil.rmtree(TestSecureShell2.STAGING_LOCAL_DIR)

        localpath, remotepath = self.shell.constructPaths(file=TestSecureShell2.STAGING_LOCAL_DIR)
        self.shell.executeCommand('rm -fr %s' % remotepath)
        return

    def testStageFile(self):
        return


    def testStageDirectory(self):

        self.shell.stageFile(TestSecureShell2.STAGING_LOCAL_DIR)


        localDirsToProcess = [TestSecureShell2.STAGING_LOCAL_DIR]
        # now verify that the files exist remotely
        for dirpath, dirnames, filenames in os.walk(TestSecureShell2.STAGING_LOCAL_DIR):
            for dirname in dirnames:
                localDirsToProcess.append(os.path.sep.join([dirpath, dirname]))
            pass

        remoteFS = self.shell.getFS()
        for localDir in localDirsToProcess:
            localpath, remotepath = self.shell.constructPaths(file=localDir)
            localFiles = os.listdir(localpath)
            localFiles.sort()
            remoteFiles = remoteFS.listdir(remotepath)
            remoteFiles.sort()
            self.assertEquals(localFiles, remoteFiles)
            pass

        return

    def testDestageDirectory(self):
        return

    def testDestageDirectory(self):
        return


    # END class TestSecureShell2
    pass


