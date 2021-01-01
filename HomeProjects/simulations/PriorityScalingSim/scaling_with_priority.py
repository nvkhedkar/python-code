import simpy
import random
from functools import wraps, partial
import re, os, sys, logging

SCRIPT_DIR = re.sub(r'\\', '/', os.path.dirname(os.path.realpath(__file__)))
SCRIPT_BASE_DIR = re.sub(r'\\', '/', os.path.dirname(SCRIPT_DIR))
FILE_NAME = f'{os.path.splitext(os.path.basename(__file__))[0]}.log'
sys.path.insert(-1, SCRIPT_DIR)
sys.path.insert(-1, SCRIPT_BASE_DIR)
import PriorityScalingSim.common as cmn

cmn.LOG_FORMAT = '{%(filename)s:%(lineno)d} %(levelname)s: %(message)s'
cmn.set_logging_config(logging.DEBUG, f'./logs/{FILE_NAME}')
logger = cmn.logger

RANDOM_SEED = 42
SIM_TIME = 58  # Simulation time in minutes

MAX_MACHINES = 5  # Number of machines in the station
MIN_MACHINES = 2
JOB_RUN_TIME = 5.
T_INTER = 7  # Create a car every ~7 minutes
MACHINE_STARTUP_TIME = 3
ENABLE_SCALING = True
MAX_IDLE_TIME = 2
LOCK_BATCH_SIZE = 1

NUM_INITIAL_CUSTOMERS = 1
NUM_CUSTOMERS = 2


def job_run_time():
    return JOB_RUN_TIME
    jrt = random.normalvariate(5, 2)
    return jrt


def customer_interval():
    return random.randint(T_INTER - 4, T_INTER + 2)


def customer_jobs(i, n=0):
    if n > 0:
        return n
    if i == 1:
        return 5
    else:
        return 3


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
    data.append(item)


monitor_data = list()
locked_machines = list()
resource_monitor_pre = partial(resource_monitor, monitor_data, 'pre')
resource_monitor_post = partial(resource_monitor, monitor_data, 'post')


class Station:
    def __init__(self, env, num_machines, jobtime=0):
        self.env = env
        self.machine = simpy.PriorityResource(env, num_machines)
        self.jobtime = jobtime
        patch_resource(self.machine,
                       # post=resource_monitor_post,
                       pre=resource_monitor_pre
                       )

    def do_job(self, job, run_time):
        yield self.env.timeout(run_time)

    def scale_machine(self, job, job_time):
        yield self.env.timeout(job_time)


class JobBase:
    def __init__(self, env, name, station, priority=10):
        self.env = env
        self.name = name
        self.station = station
        self.priority = priority

    @classmethod
    def get_resource_status(cls):
        locked = len(locked_machines)
        num_running = monitor_data[-1]["running"] - locked
        if num_running < 0:
            num_running = 0
        running = f'{num_running}/{MAX_MACHINES}'
        queued = monitor_data[-1]["jobs_queued"]
        return f'[time: {"{:.2f}".format(env.now)} running: {running}  queued: {queued} locked: {locked}]'


class Job(JobBase):
    def __init__(self, env, name, station, priority=10):
        super().__init__(env, name, station, priority)
        self.arrival = 0
        self.start = 0
        self.end = 0

    def run(self, run_time=JOB_RUN_TIME):
        self.arrival = env.now
        logger.info('%s (%d) submitted at %.2f. %s' % (
            self.name, self.priority, self.arrival, self.get_resource_status()))
        with self.station.machine.request(priority=self.priority) as request:
            yield request
            self.start = env.now
            logger.info('%s (%d) starts at %.2f. %s' % (self.name, self.priority, self.start, self.get_resource_status()))
            yield env.process(self.station.do_job(self.name, job_run_time()))
            self.end = env.now
            logger.info('%s (%d) Finished at %.2f. %s' % (self.name, self.priority, env.now, self.get_resource_status()))


class ScaleJob(JobBase):
    def __init__(self, env, name, station, priority=10):
        super().__init__(env, name, station, priority)
        self.scaled_process = None
        self.released = False
        self.arrival = 0
        self.start = 0
        self.end = 0

    def scale_job(self, processes, run_time=SIM_TIME + 2):
        self.arrival = env.now
        with self.station.machine.request(priority=self.priority) as request:
            yield request
            try:
                self.start = env.now
                logger.info('%s (%d) Locked machine at %.2f. %s' % (
                    self.name, self.priority, self.start, self.get_resource_status()))
                self.scaled_process = env.process(self.station.scale_machine(self.name, run_time))
                processes.append(self.scaled_process)
                yield self.scaled_process
                self.end = env.now
            except simpy.Interrupt as si:
                logger.debug('Release resource: {} {:.2f}'.format(si.cause, env.now))
                sm.update_locking_history('Machine Starting: ' + self.get_resource_status())
                yield env.timeout(MACHINE_STARTUP_TIME)
                logger.info('Release resource Done {} {:.2f} {}'.format(
                    self.name, env.now, self.get_resource_status()))
                sm.update_locking_history('Machine Started: ' + self.get_resource_status())
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
                logger.debug('terminated')


class ScalingControl(Customer):
    def __init__(self, name, station):
        super().__init__(name, station)
        self.lock_jobs = list()
        self.all_idle_times = list()
        self.num_lock_jobs = 0
        # self.active_machines = list()
        # self.num_active_machines = 0
        # self.num_unlock_jobs = 0

    # def set_active_machine(self, ):
    #     proc = env.process(self.active_machine())
    #     self.num_active_machines += 1
    #     machine_id = f'M-{format(self.num_active_machines, "05d")}'
    #     scaled_machine = ScaledMachine(machine_id, 'active', proc, env.now)
    #     self.active_machines.append(scaled_machine)

    def active_machine(self):
        while True:
            try:
                yield env.timeout(1)
            except simpy.Interrupt:
                logger.debug('Machine deactivated')
                # self.active_machines.remove(scaled_machine)

    def get_num_to_release(self, jobs_in_queue):
        jobs_per_mc = jobs_in_queue / MAX_MACHINES - len(locked_machines)
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
                    logger.debug('jobs_in_queue {} locked {} time {:.2f}'.format(
                        jobs_in_queue, len(locked_machines), env.now))
                    rj = locked_machines.pop()
                    rj.interrupt("start_machine")
                    # self.set_active_machine()
                    offset = MACHINE_STARTUP_TIME

    def get_idle_machines(self):
        running_jobs = monitor_data[-1]['running'] - len(locked_machines)
        available_machines = MAX_MACHINES - len(locked_machines)
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
            sm.update_total_idle_time(idle_machines)

    def scale_down(self):
        offset = 0
        while True:
            yield env.timeout(1 + offset)
            idle_machines, machines_to_lock = self.get_idle_machines()
            self.set_idle_times(idle_machines)
            if env.now > 15:
                logger.debug("scale_down {} {} {}".format(
                    idle_machines, machines_to_lock, self.all_idle_times))
            if idle_machines > 0 and machines_to_lock > 0:
                num_unlocked = 0
                for idle_time in self.all_idle_times:
                    if idle_time > MAX_IDLE_TIME and num_unlocked < LOCK_BATCH_SIZE:
                        self.num_lock_jobs += 1
                        cj = ScaleJob(env, f'{self.name}_LockJob_%d' % self.num_lock_jobs, self.station, priority=0)
                        self.lock_jobs.append(cj)
                        cjp = env.process(cj.scale_job(locked_machines))
                        sm.update_locking_history('Machine Stopped: ' + JobBase.get_resource_status())
                        num_unlocked += 1

    def create_jobs(self, n=(MAX_MACHINES - MIN_MACHINES)):
        prefix = 'LockJob'
        if ENABLE_SCALING:
            csc = env.process(self.scale_up())
            csd = env.process(self.scale_down())

        for i in range(MAX_MACHINES - MIN_MACHINES):
            self.num_lock_jobs += 1
            cj = ScaleJob(env, f'{self.name}_{prefix}_%d' % self.num_lock_jobs, self.station, priority=0)
            self.lock_jobs.append(cj)
            cjp = env.process(cj.scale_job(locked_machines))


class SimMonitor:
    def __init__(self, e):
        self.env = e
        self.customers = list()
        self.scaling_control = list()
        self.jobs = list()
        self.locked_machines = list()
        self.locking_history = list()
        self.resource_status = dict()
        self.total_idle_time = 0
        self.total_compute_time = 0

    def summarize_simulation(self):
        self.show_customer_summary()
        self.show_scaling_summary()
        logger.info('Total idle time: {}'.format(self.total_idle_time))
        self.calculate_compute_time()
        logger.info('Total compute time: {}'.format(self.total_compute_time))
        for lh in self.locking_history:
            logger.info(lh)

    def update_total_idle_time(self, all_idle_times):
        self.total_idle_time += all_idle_times

    def update_locking_history(self, status):
        self.locking_history.append(status)

    def calculate_compute_time(self):
        for c in self.customers:
            for j in c.jobs:
                if j.end > 0 and j.end >= j.start:
                    self.total_compute_time += (j.end - j.start)

    def show_customer_summary(self):
        for c in self.customers:
            for j in c.jobs:
                logger.info('%s, %s, %.2d, %.2f, %.2f, %.2f' % (
                    c.name, j.name, j.priority, j.arrival, j.start, j.end))

    def show_scaling_summary(self):
        for sc in self.scaling_control:
            for j in sc.lock_jobs:
                logger.info('%s, %s, %.2d, %.4d, %.4d, %.4d' % (
                    sc.name, j.name, j.priority, j.arrival, j.start, j.end))


class SetupSim:
    def __init__(self, env, num_machines, jobtime, t_inter):
        # self.customers = list()
        # self.jobs = list()
        self.env = env
        self.n_machines = num_machines
        self.job_time = jobtime
        self.job_interval = t_inter
        self.station = Station(self.env, self.n_machines, self.job_time)

    def setup_scaling_control(self):
        scaling_control = ScalingControl('DC0', self.station)
        sm.scaling_control.append(scaling_control)
        scaling_control.create_jobs()

    def setup_customers(self, n=1):
        start = env.now
        i = 0
        self.setup_scaling_control()

        for i in range(NUM_INITIAL_CUSTOMERS):
            customer = Customer('C%d' % (i + 1), self.station)
            sm.customers.append(customer)
            customer.create_jobs(customer_jobs(i))
        # self.add_jobs(customer)

        for j in range(i + 1, NUM_CUSTOMERS + 1):
            yield env.timeout(customer_interval())
            customer = Customer('C%d' % (j + 1), self.station)
            sm.customers.append(customer)
            # jn = 3
            # if j == 1:
            #     jn = 5
            customer.create_jobs(customer_jobs(j))
            # self.add_jobs(customer)

        while True:
            yield env.timeout(1)
            if (env.now - start) >= 25:
                sm.customers[-1].create_jobs(customer_jobs(0, n=6))
                break


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
        env.process(cj.run())  # job(env, jobs, f'{prefix} %d' % i, station))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 4, t_inter + 2))
        i += 1
        p = 10 - i
        logger.info(f"Created {prefix} %d (%d) at %.2f" % (i, p, env.now))
        cj = Job(env, f'{prefix} %d' % i, station, priority=p)
        jobs.append(cj)
        env.process(cj.run())  # job(env, jobs, f'{prefix} %d' % i, station, priority=p))


def show_customer_summary():
    for c in customers:
        for j in c.jobs:
            logger.info('%s, %s, %.2d, %.4d, %.4d, %.4d' % (c.name, j.name, j.priority, j.arrival, j.start, j.end))


logger.info('station')
logger.info('Check out http://youtu.be/fXXmeP9TvBg while simulating ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
all_jobs = []
customers = []
sm = SimMonitor(env)
monitor = SetupSim(env, MAX_MACHINES, JOB_RUN_TIME, T_INTER)
env.process(
    monitor.setup_customers())  # setup_customers(env, NUM_MACHINES, JOBTIME, T_INTER))  # setup(env, all_jobs, NUM_MACHINES, JOBTIME, T_INTER))
# Execute!
env.run(until=SIM_TIME)
sm.summarize_simulation()
logger.info(len(monitor_data))  # json.dumps(monitor_data, indent=2))
