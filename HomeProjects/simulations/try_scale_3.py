import simpy
from functools import wraps, partial


SIM_TIME = 100


class MonitoredResource(simpy.PriorityResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []

    def request(self, *args, **kwargs):
        self.data.append((self._env.now, self.count, len(self.queue)))
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.data.append((self._env.now, self.count, len(self.queue)))
        return super().release(*args, **kwargs)

    def put(self, *args, **kwargs):
        self.data.append((self._env.now, self.count, len(self.queue)))
        return super().put()

    def get(self, *args, **kwargs):
        self.data.append((self._env.now, self.count, len(self.queue)))
        return super().get()


def patch_resource(resource, pre=None, post=None):
    """Patch *resource* so that it calls the callable *pre* before each
    put/get/request/release operation and the callable *post* after each
    operation.  The only argument to these functions is the resource
    instance.
    """
    def get_wrapper(func):
        # Generate a wrapper for put/get/request/release
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This is the actual wrapper
            # Call "pre" callback
            if pre:
                pre(resource)

            # Perform actual operation
            ret = func(*args, **kwargs)

            # Call "post" callback
            if post:
                post(resource)

            return ret
        return wrapper

    # Replace the original operations with our wrapper
    for name in ['put', 'get', 'request', 'release']:
        if hasattr(resource, name):
            setattr(resource, name, get_wrapper(getattr(resource, name)))


def resource_monitor(data, prefix, resource):
    """This is our monitoring callback."""
    item = (
        resource._env.now,  # The current simulation time
        resource.count,  # The number of users
        len(resource.queue),  # The number of queued processes
    )
    print('Monitor', prefix, item)
    data.append(item)


monitor_data = list()
resource_monitor_pre = partial(resource_monitor, monitor_data, 'pre')
resource_monitor_post = partial(resource_monitor, monitor_data, 'post')


def test_process(env, res):
    with res.request() as req:
        yield req
        yield env.timeout(1)


def setup_machines():
    machine = simpy.PriorityResource(env, 4)
    patch_resource(machine,
                   # post=resource_monitor_post,
                   pre=resource_monitor_pre
                   )
    return machine


def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = SIM_TIME
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start


env = simpy.Environment()
machines = setup_machines()
env.run()

