import simpy
import random
from functools import wraps, partial

RANDOM_SEED = 42
NUM_MACHINES = 5  # Number of machines in the station
MIN_MACHINES = 2
JOBTIME = 5      # Minutes it takes to clean a car
T_INTER = 7       # Create a car every ~7 minutes
SIM_TIME = 58     # Simulation time in minutes
STARTUP_TIME = 3
ENABLE_SCALING = False
MAX_IDLE_TIME = 2
LOCK_BATCH = 1

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
    item = {
        "time": resource._env.now,  # The current simulation time
        "running": resource.count,  # The number of users
        "jobs_queued": len(resource.queue),  # The number of queued processes
    }
    # print('Monitor', prefix, item)
    data.append(item)


monitor_data = list()
locked_machines = list()
resource_monitor_pre = partial(resource_monitor, monitor_data, 'pre')
resource_monitor_post = partial(resource_monitor, monitor_data, 'post')


class Station(object):
    """A station has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_machines, jobtime):
        self.env = env
        self.machine = simpy.PriorityResource(env, num_machines)
        patch_resource(self.machine,
                       # post=resource_monitor_post,
                       pre=resource_monitor_pre
                       )
        self.jobtime = jobtime

    def do_job(self, job):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(self.jobtime)
        # print("station removed %d%% of %s's dirt." %
        #       (random.randint(50, 99), car))

    def scale_machine(self, job, job_time):
        yield self.env.timeout(job_time)


class JobBase:
    def __init__(self, env, name, station, priority=10):
        self.env = env
        self.name = name
        self.station = station
        self.priority = priority

    def get_resource_status(self):
        locked = len(locked_machines)
        num_running = monitor_data[-1]["running"] - locked
        if num_running < 0:
            num_running = 0
        running = f'{num_running}/{NUM_MACHINES}'
        queued = monitor_data[-1]["jobs_queued"]
        return f' running: {running}  queued: {queued} locked: {locked}'


class Job(JobBase):
    def __init__(self, env, name, station, priority=10):
        super().__init__(env, name, station, priority)
        self.arrival = 0
        self.start = 0
        self.end = 0

    def run(self):
        self.arrival = env.now
        print('%s (%d) submitted at %.2f. [%s]' % (self.name, self.priority, self.arrival, self.get_resource_status()))
        with self.station.machine.request(priority=self.priority) as request:
            yield request
            self.start = env.now
            print('%s (%d) starts at %.2f. [%s]' % (self.name, self.priority, self.start, self.get_resource_status()))
            yield env.process(self.station.do_job(self.name))
            self.end = env.now
            print('%s (%d) Finished at %.2f. [%s]' % (self.name, self.priority, env.now, self.get_resource_status()))


class ScaleJob(JobBase):
    def __init__(self, env, name, station, priority=10):
        super().__init__(env, name, station, priority)
        self.scaled_process = None
        self.released = False
        self.arrival = 0
        self.start = 0
        self.end = 0

    def scale_job(self, processes, run_time=SIM_TIME+2):
        self.arrival = env.now
        with self.station.machine.request(priority=self.priority) as request:
            yield request
            try:
                self.start = env.now
                print('%s (%d) Locked machine at %.2f. [%s]' % (
                    self.name, self.priority, self.start, self.get_resource_status()))
                self.scaled_process = env.process(self.station.scale_machine(self.name, run_time))
                processes.append(self.scaled_process)
                yield self.scaled_process
                self.end = env.now
            except simpy.Interrupt as si:
                print('Release resource:', si.cause, env.now)
                yield env.timeout(STARTUP_TIME)
                print('Release resource Done ', self.name, env.now, self.get_resource_status())
                self.end = env.now
        return


class Customer:
    def __init__(self, name, station):
        self.name = name
        self.jobs = list()
        self.job_num = 0
        self.station = station

    def calculate_priority(self, i, n):
        return 0 + i

    def create_jobs(self, n):
        prefix = 'Job'
        for i in range(n):
            cj = Job(env, f'{self.name}_{prefix}_%d' % self.job_num, self.station,
                     priority=0  # self.calculate_priority(i, n)
                     )
            self.job_num += 1
            self.jobs.append(cj)
            env.process(cj.run())  # job(env, jobs, f'{prefix} %d' % i, station))


class ScaledMachine:
    def __init__(self, mid='', state='none', process=None, st=0.):
        self.id = mid
        self.state = 'active'
        self.idle_time = 0
        self.start_time = st
        self.process = process

    def active_process(self):
        while True:
            try:
                yield env.timeout(1)
            except simpy.Interrupt:
                print('terminated')

class ScalingControl(Customer):
    def __init__(self, name, station):
        super().__init__(name, station)
        self.lock_jobs = list()
        self.all_idle_times = list()
        self.idle_time = {
            'n_machines': 0,
            'time': 0,
        }
        self.active_machines = list()
        self.machine_stats = {
            'active': 0,
            'idle': 0,
            'time': 0,
        }
        self.num_active_machines = 0
        self.num_lock_jobs = 0
        self.num_unlock_jobs = 0

    def set_active_machine(self, ):
        proc = env.process(self.active_machine())
        self.num_active_machines += 1
        machine_id = f'M-{format(self.num_active_machines, "05d")}'
        scaled_machine = ScaledMachine(machine_id, 'active', proc, env.now)
        self.active_machines.append(scaled_machine)

    def active_machine(self):
        while True:
            try:
                yield env.timeout(1)
            except simpy.Interrupt:
                print('Machine deactivated')
                # self.active_machines.remove(scaled_machine)

    def get_num_to_release(self, jobs_in_queue):
        jobs_per_mc = jobs_in_queue / NUM_MACHINES - len(locked_machines)
        num_to_release = 0
        if jobs_in_queue > 2:
            num_to_release = 1
        if jobs_in_queue > 4:
            num_to_release = 2
        if num_to_release > len(locked_machines):
            num_to_release = len(locked_machines)
        return num_to_release

    def scale_up(self):
        offset = 0
        while True:
            yield env.timeout(1 + offset)
            offset = 0
            if locked_machines:
                jobs_in_queue = monitor_data[-1]['jobs_queued']
                for i in range(self.get_num_to_release(jobs_in_queue)):
                    print('jobs_in_queue {} locked {} time {:.2f}'.format(jobs_in_queue, len(locked_machines), env.now))
                    rj = locked_machines.pop()
                    rj.interrupt("start_machine")
                    # self.set_active_machine()
                    offset = STARTUP_TIME

    def get_idle_machines(self):
        running_jobs = monitor_data[-1]['running'] - len(locked_machines)
        available_machines = NUM_MACHINES - len(locked_machines)
        idle_machines = available_machines - running_jobs
        machines_to_lock = 0
        if idle_machines > MIN_MACHINES:
            machines_to_lock = idle_machines - MIN_MACHINES
        return idle_machines, machines_to_lock

    def set_idle_times(self, idle_machines):
        idle_times = len(self.all_idle_times)
        if idle_machines == 0:
            if idle_times > 0:
                self.all_idle_times[:] = []
                idle_times = 0
            else:
                return
        else:
            if idle_times == 0:
                for i in range(idle_machines):
                    self.all_idle_times.append(1)
            elif idle_times == idle_machines:
                for i in range(idle_machines):
                    self.all_idle_times[i] += 1
            elif idle_times < idle_machines:
                for i, idle_time in enumerate(self.all_idle_times):
                    self.all_idle_times[i] += 1
                for i in range(idle_times, idle_machines):
                    self.all_idle_times.append(1)
            elif idle_times > idle_machines:
                i = random.randint(0, idle_times)
                del self.all_idle_times[i]
                for i in range(idle_machines):
                    self.all_idle_times[i] += 1

    def scale_down(self):
        offset = 0
        while True:
            yield env.timeout(1 + offset)
            idle_machines, machines_to_lock = self.get_idle_machines()
            self.set_idle_times(idle_machines)
            if env.now > 15:
                print("scale_down", idle_machines, machines_to_lock, self.all_idle_times)
            if idle_machines > 0 and machines_to_lock > 0:
                num_unlocked = 0
                for idle_time in self.all_idle_times:
                    if idle_time > MAX_IDLE_TIME and num_unlocked < LOCK_BATCH:
                        self.num_lock_jobs += 1
                        cj = ScaleJob(env, f'{self.name}_LockJob_%d' % self.num_lock_jobs, self.station, priority=0)
                        self.lock_jobs.append(cj)
                        cjp = env.process(cj.scale_job(locked_machines))
                        num_unlocked += 1

    def scale_down_bad(self):
        offset = 0
        while True:
            yield env.timeout(1 + offset)
            running_jobs = monitor_data[-1]['running']
            idle_machines = NUM_MACHINES - (len(locked_machines) + running_jobs)
            machines_to_lock = idle_machines - len(locked_machines)
            if idle_machines > 0:
                self.idle_time['n_machines'] = idle_machines
                self.idle_time['time'] += 1 + offset
                print('Idle machines: {} time {} {:.2f}'. format(idle_machines, self.idle_time['time']))
                if self.idle_time['time'] > MAX_IDLE_TIME and machines_to_lock > 0:
                    self.num_lock_jobs += 1
                    cj = ScaleJob(env, f'{self.name}_LockJob_%d' % self.num_lock_jobs, self.station, priority=0)
                    self.lock_jobs.append(cj)
                    cjp = env.process(cj.scale_job(locked_machines))

    def create_jobs(self, n):
        prefix = 'LockJob'
        if ENABLE_SCALING:
            csc = env.process(self.scale_up())
            csd = env.process(self.scale_down())

        for i in range(n):
            self.num_lock_jobs += 1
            cj = ScaleJob(env, f'{self.name}_{prefix}_%d' % self.num_lock_jobs, self.station, priority=0)
            self.lock_jobs.append(cj)
            cjp = env.process(cj.scale_job(locked_machines))


class Monitor:
    def __init__(self, env, num_machines, jobtime, t_inter):
        self.customers = list()
        self.jobs = list()
        self.env = env
        self.n_machines = num_machines
        self.job_time = jobtime
        self.job_interval = t_inter
        self.station = Station(self.env, self.n_machines, self.job_time)
        self.dummy_customer = None

    def setup_dummy_customer(self):
        self.dummy_customer = ScalingControl('DC0', self.station)
        self.dummy_customer.create_jobs(NUM_MACHINES - MIN_MACHINES)

    def setup_customers(self, n=1):
        start = env.now
        time_elapsed = 0
        i = 0
        self.setup_dummy_customer()
        customer = Customer('C0', self.station)
        self.customers.append(customer)
        customer.create_jobs(3)
        # self.add_jobs(customer)
        i += 1

        for i in range(1, 3):
            yield env.timeout(random.randint(self.job_interval - 4, self.job_interval + 2))
            customer = Customer('C%d' % (i + 1), self.station)
            self.customers.append(customer)
            jn = 3
            if i == 1:
                jn = 5
            customer.create_jobs(jn)
            # self.add_jobs(customer)

        while True:
            yield env.timeout(1)
            if (env.now - start) >= 25:
                customer.create_jobs(6)
                break

    def add_jobs(self, customer):
        if len(self.jobs) == 0:
            [self.jobs.append(j) for j in customer.jobs]
        else:
            self.jobs.extend(customer.jobs)

    def show_customer_summary(self):
        for c in self.customers:
            for j in c.jobs:
                print('%s, %s, %.2d, %.4d, %.4d, %.4d' % (c.name, j.name, j.priority, j.arrival, j.start, j.end))


def job(env, jobs, name, cw, priority=10):
    """The car process (each car has a ``name``) arrives at the station
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back 

    """
    print('%s (%d) arrives at the station at %.2f.' % (name, priority, env.now))
    with cw.machine.request(priority=priority) as request:
        yield request

        print('%s (%d) starts washing at %.2f.' % (name, priority, env.now))
        yield env.process(cw.wash(name))

        print('%s (%d) leaves the station at %.2f.' % (name, priority, env.now))


def setup_customers(env, num_machines, washtime, t_inter):
    station = Station(env, num_machines, washtime)
    i = 0
    customer = Customer('C_0', station)
    customers.append(customer)
    customer.create_jobs(3)
    i += 1

    for i in range(1, 3):
        yield env.timeout(random.randint(t_inter - 4, t_inter + 2))
        customer = Customer('C_%d' % (i + 1), station)
        customers.append(customer)
        jn = 3
        if i == 1:
            jn = 5
        customer.create_jobs(jn)


def setup(env, jobs, num_machines, washtime, t_inter):
    """Create a station, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the station
    prefix = 'Job'
    station = Station(env, num_machines, washtime)
    # customer = Customer('C1', station)
    # customers.append(customer)
    # customer.create_jobs(2)
    # Create 4 initial cars
    for i in range(2):
        cj = Job(env, f'{prefix} %d' % i, station)
        jobs.append(cj)
        env.process(cj.run())  #job(env, jobs, f'{prefix} %d' % i, station))


    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 4, t_inter + 2))
        i += 1
        p = 10 - i
        print(f"Created {prefix} %d (%d) at %.2f" % (i, p, env.now))
        cj = Job(env, f'{prefix} %d' % i, station, priority=p)
        jobs.append(cj)
        env.process(cj.run())  # job(env, jobs, f'{prefix} %d' % i, station, priority=p))


# def show_summary(jobs):
#     print('%s, %s, %s, %s')
#     for j in jobs:
#         print('%s, %.2d, %.4d, %.4d, %.4d' % (j.name, j.priority, j.arrival, j.start, j.end))


def show_customer_summary():
    for c in customers:
        for j in c.jobs:
            print('%s, %s, %.2d, %.4d, %.4d, %.4d' % (c.name, j.name, j.priority, j.arrival, j.start, j.end))


print('station')
print('Check out http://youtu.be/fXXmeP9TvBg while simulating ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
all_jobs = []
customers = []
monitor = Monitor(env, NUM_MACHINES, JOBTIME, T_INTER)
env.process(monitor.setup_customers())  # setup_customers(env, NUM_MACHINES, JOBTIME, T_INTER))  # setup(env, all_jobs, NUM_MACHINES, JOBTIME, T_INTER))
# Execute!
env.run(until=SIM_TIME)
monitor.show_customer_summary()
import json
print(len(monitor_data))  # json.dumps(monitor_data, indent=2))
