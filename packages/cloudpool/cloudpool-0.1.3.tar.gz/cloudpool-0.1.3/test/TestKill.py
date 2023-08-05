import os
import threadpool
import time
import unittest

import cloudpool as PoolModule
import cloudpool.shell as ShellModule
import cloudpool.task as TaskModule


def doTask(*args, **kwds):

    task = kwds['task']

    return task.do()

class TestKill(unittest.TestCase):
    pass


class TestKillLocal(TestKill):

    def setUp(self):
        self.pool = PoolModule.Pool(1)
        self.env = ShellModule.LocalShell()
        return

    def testKill(self):

        task = TaskModule.Task()
        commandBuilder = TaskModule.CommandBuilder()

        commandToExecute = [
            os.path.sep.join(['.','resources','testdata','TestShell','sleep.py'])
            ]

        kwds = {}
        kwds['command to execute'] = commandToExecute
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

        time.sleep(3)
        self.env.kill(task)

        self.pool.wait()
        assert request.exception

        return

    pass


class TestKillSsh(TestKill):
    pass


class TestKillPython(TestKill):
    pass
