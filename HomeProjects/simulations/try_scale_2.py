import simpy
from random import randint

SIM_TIME = 100


class LockableMachine:
    def __init__(self, env):
        self.env = env
        # self.drive_proc = env.process(self.lock_machine(env))

    def lock_machine(self, env):
        while True:
            locked = env.process(self.lock_this(env))
            parking = env.timeout(60)
            if not locked.triggered:
                locked.interrupt('Start machine')

    def do_job(self, env):
        while True:
            # Drive for 20-40 min
            yield env.timeout(randint(20, 40))

            # Park for 1 hour
            print('Start parking at', env.now)
            locked = env.process(self.lock_this(env))
            parking = env.timeout(60)
            yield locked | parking
            if not locked.triggered:
                # Interrupt charging if not already done.
                locked.interrupt('Need to go!')
            print('Stop parking at', env.now)

    def lock_this(self, env):
        print('Locking machine: ', env.now)
        try:
            yield env.timeout(SIM_TIME)
            print('release machine: ', env.now)
        except simpy.Interrupt as i:
            yield env.timeout(10)
            print('Force release: ', env.now, 'msg:',
                  i.cause)


env = simpy.Environment()
ev = LockableMachine(env)
dp = env.process(ev.lock_machine(env))
env.run(until=SIM_TIME)
