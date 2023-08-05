import logging

class Environment(object):
    
    def execute(self, task, *args, **kargs):
        raise NotImplemented(
            'have not implemented %s.execute()' % self.__class__)

    def kill(self, task, *args, **kargs):
        raise NotImplemented(
            'have not implemented %s.kill()' % self.__class__)
 
    def getCommandBuilder(self, task):
        return task.getCommandBuilder()
    
    # END class Environment
    pass




class PythonEval(Environment):

    DEFAULT_COMMANDBUILDER_TYPE = 'python eval'
    
    
    def execute(self, task, *args, **kargs):
        request = task.workRequest()
        
        commandBuilder = self.getCommandBuilder(task)

        command = commandBuilder.buildCommand(task)

        request.kwds['executed command'] = command
        
        logging.debug('%s executing command "%s"' % (self.__class__, command))
        evalResult = eval(command)

        request.kwds['eval result'] = evalResult
        
        return 0
    
    # TODO:
    # implement the following
    # the question is, if this is a python eval
    # and it's taking too long,
    # is there a way to kill it?
    # def kill(self, task, *args, **kwds):
    #     raise NotImplementedError

    # END class PythonEval
    pass
