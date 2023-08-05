import os
import sys
import threadpool
import unittest
import logging
import tempfile

import cloudpool as PoolModule
import cloudpool.environment as EnvironmentModule
import cloudpool.shell as ShellModule
import cloudpool.task as TaskModule
import cloudpool.utils as UtilsModule



def doTask(*args, **kwds):

    task = kwds['task']

    return task.do()


class TestExecuteLocal(unittest.TestCase):

    FILE_TO_CREATE = 'TestExecute.TestExecuteLocal.testExecute1'

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

        self.pool = PoolModule.Pool(1)

        # setup the execution environment
        self.env = ShellModule.LocalShell()
        return

    def tearDown(self):

        path = self.constructFullPath(TestExecuteLocal.FILE_TO_CREATE)
        if os.path.exists(path):
            os.unlink(path)

        if os.path.exists(self.tmpdir):
            os.rmdir(self.tmpdir)

        return

    def constructFullPath(self, localPath):
        return os.path.sep.join([self.tmpdir, localPath])


    def testExecute1(self):

        path = self.constructFullPath(TestExecuteLocal.FILE_TO_CREATE)

        assert not os.path.exists(path)

        task = TaskModule.Task()
        commandBuilder = TaskModule.CommandBuilder()

        kwds = {}
        kwds['command to execute'] = ['touch', path]
        kwds['task'] = task
        kwds['execute environment'] = self.env
        kwds['command builder map'] = {
            'shell process':commandBuilder
        }

        # the actual execution of the task will call
        # doTask(*args, **kwds)
        request = threadpool.WorkRequest(
            doTask,
            args = [],
            kwds = kwds,
        )
        task.workRequest(request)

        self.pool.putRequest(request)
        self.pool.wait()
        
        assert not request.exception
        assert os.path.exists(path)
        return


    # END class TestExecuteLocal
    pass


class TestExecuteSsh(unittest.TestCase):

    FILE_TO_CREATE = 'TestExecute.TestExecuteSsh.testExecute1'

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

        self.pool = PoolModule.Pool(1)

        # setup the connection
        import test.TestShell as TestShellModule

        self.env = TestShellModule.TestSecureShell.getShell()
        self.env.establishConnection()

        self.fs = self.env.getFS()

        # setup the tmpdir path on the file system
        # for now, we hardcode to /tmp
        self.tmpdir = os.sep.join(['', 'tmp'])

        path = self.constructFullPath(TestExecuteSsh.FILE_TO_CREATE)
        if self.fileExists(path):
            self.removeFile(path)

        return


    def tearDown(self):

        path = self.constructFullPath(TestExecuteSsh.FILE_TO_CREATE)
        localpath, remotepath = self.env.constructPaths(path)
        self.fs.remove(remotepath)

        self.env.disconnect()
        return

    def constructFullPath(self, localPath):
        return os.path.sep.join([self.tmpdir, localPath])


    def fileExists(self, file):
        try:
            self.fs.open(file)
        except IOError:
            return False
        return True

    def removeFile(self, file):
        try:
            self.fs.remove(file)
        except IOError:
            pass
        return

    def testExecute1(self):

        path = self.constructFullPath(TestExecuteSsh.FILE_TO_CREATE)

        assert not self.fileExists(path)

        task = TaskModule.Task()
        commandBuilder = TaskModule.CommandBuilder()

        kwds = {}
        kwds['command to execute'] = ['touch', path]
        kwds['task'] = task
        kwds['execute environment'] = self.env
        kwds['command builder map'] = {
            'shell process':commandBuilder
        }

        # the actual execution of the task will call
        # doTask(*args, **kwds)
        request = threadpool.WorkRequest(
            doTask,
            args = [],
            kwds = kwds,
        )
        task.workRequest(request)

        self.pool.putRequest(request)
        self.pool.wait()
        
        assert not request.exception
        assert self.fileExists(path)
        return


    # END class TestExecuteSsh
    pass


class TestPythonEval(unittest.TestCase):
    
    def setUp(self):

        self.pool = PoolModule.Pool(1)

        # setup the execution environment
        self.env = EnvironmentModule.PythonEval()
        
        return
    
    def tearDown(self):
        return
    
    def testExecute1(self):

        task = TaskModule.Task()
        commandBuilder = TaskModule.CommandBuilder()

        kwds = {}
        kwds['command to execute'] = '5'
        kwds['task'] = task
        kwds['execute environment'] = self.env
        kwds['command builder map'] = {
            'shell process':commandBuilder,
            'python eval':commandBuilder
        }

        # the actual execution of the task will call
        # doTask(*args, **kwds)
        request = threadpool.WorkRequest(
            doTask,
            args = [],
            kwds = kwds,
        )
        task.workRequest(request)

        self.pool.putRequest(request)
        self.pool.wait()
        
        assert not request.exception

        assert kwds['executed command'] == kwds['command to execute']
        assert kwds['eval result'] is 5
                    
        return
    
    
    # END class TestPythonEval
    pass

def main():
    UtilsModule.configLogging()

    suite = unittest.TestSuite()
    
    suite.addTest(unittest.makeSuite(TestExecuteLocal, 'test'))
    # suite.addTest(unittest.makeSuite(TestExecuteSsh, 'test'))
    suite.addTest(unittest.makeSuite(TestPythonEval, 'test'))
    
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
    return

if __name__=="__main__":
    main()

