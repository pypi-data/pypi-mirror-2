
import cloudpool.environment as EnvironmentModule

import pomsets.resource as ResourceModule


from celery.decorators import task


# TODO:
# implement this decorated function execute the task
@task
def execute_task(env, task, *args, **kwds):
    env.execute(task, *args, **kwds)
    return


class Pool(ResourceModule.Struct):

    ATTRIBUTES = [
        'workRequests'
        ]

    def __init__(self):
        ResourceModule.Struct.__init__(self)
        self.workRequests({})
        return

    def isEmpty(self):
        # TODO:
        # need a way to determine if there are nodes
        # in the celery cluster
        return False

    def putRequest(self, request, block=True, timeout=None):
        """
        Put work request into work queue and save its id for later.

        NOTE: most of this function duplicates threadpool.ThreadPool.putRequest
        except for the actually putting into the request queue
        """

        assert isinstance(request, WorkRequest)
        # don't reuse old work requests
        assert not getattr(request, 'exception', None)

        # self._requests_queue.put(request, block, timeout)
        # TODO:
        if True:
            raise NotImplementedError('putting the request in the queue')

        self.workRequests()[request.requestID] = request


    # END class Pool
    pass


class Environment(EnvironmentModule.Environment, ResourceModule.Struct):
    """
    This celery.Environment class executes 
    locally on the pomsets app host,
    while celery.Environment.environment() 
    will execute on the celery worker host
    """
    
    ATTRIBUTES = [
        'environment'
        ]

    def __init__(self):
        EnvironmentModule.Environment.__init__(self)
        ResourceModule.Struct.__init__(self)
        return

    def execute(self, task, *args, **kargs):
        result = execute_task.delay(self.environment(), task, *args, **kwds)

        # this waits for the execution
        returnValue = result.get()
        if not result.successful():
            raise result.result
        return returnValue

    # END class Environment
    pass
