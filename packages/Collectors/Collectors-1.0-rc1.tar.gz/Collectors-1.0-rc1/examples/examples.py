# encoding: utf-8

from collectors import Collector, get

def simpy_example():
    """Shows the general usage of *Collectors*."""
    import random

    import matplotlib.pyplot as plt
    from numpy import array, float64
    from SimPy.Simulation import Simulation, Process, hold

    from collectors import Collector, get, manual


    class MyProc(Process):
        """A simple example process that illustrates the usage of the new
        monitoring approach."""
        def __init__(self, sim):
            Process.__init__(self, sim=sim)

            self.a = 0
            self.b = 0
            self.c = 0

            # Create a monitor that will collect:
            # time:     A list with timestampes from sim.now()
            # a:        Values of proc.a
            # b:        Values of proc.b
            # diff:     A value passed manually
            # square:   Square of self.c
            self.monitor = Collector(
                ('time', sim.now),
                get(self, 'a', 'b'),
                ('diff', manual),
                ('square', lambda: self.c ** 2),
            )

        def run(self):
            while True:
                self.a += random.random()
                self.b += random.randint(1, 2)
                self.c += random.randint(2, 4)

                self.monitor(diff=self.c-self.b)

                yield hold, self, 2


    # Run the simulation
    sim = Simulation()
    proc = MyProc(sim)
    sim.activate(proc, proc.run())
    sim.simulate(until=10)

    # Just a test and a simple example how to acces the monitored values:
    assert proc.monitor[1] == proc.monitor.a

    print proc.monitor
    print zip(*proc.monitor)

    # NumPy helps you with the statistics and other calculations.
    # Note: specification of dtype gives you a massive speed-up!
    a = array(proc.monitor.a, dtype=float64)
    print 'a:', a
    # NumPy: average, std. deviation, variance
    print 'a stats:', a.mean(), a.std(), a.var()

    # This one creates a multi-dimensional array (see the output)
    np_mon = array(proc.monitor, dtype=float64)
    print 't, a, b, diff, square:\n', np_mon
    # Get the average of all monitored proc.b
    print 'b stats:', np_mon[2].mean()
    # Get the std. deviation of all monitored proc.c
    print 'c stats:', np_mon[3].std()

    # Matplotlib plots your data:
    # Either directly from a monitor ...
    plt.plot(proc.monitor.time, proc.monitor.a, 'b')
    # ... or the NumPy array
    plt.plot(np_mon[0], np_mon[2], 'r')
    plt.show()
    
def simpy_example2():
    from SimPy.Simulation import Simulation, Process, hold
    from collectors import Collector, get_objects
    
    class MyProc2(Process):
        """docstring for MyProc2"""
        def __init__(self, sim, pid):
            Process.__init__(self, sim=sim)
            self._pid = 'p%d' % pid
            self.a = 0
            
        def run(self):
            while True:
                self.a += 1

    sim = Simulation()
    procs = [MyProc2(sim, i) for i in range(10)]
    for proc in procs:
        sim.activate(proc, proc.run())
        
    # This collector will have the attributes "t", "p0_a", "p1_a", ..., "p9_a"
    # and monitor the simulation time as well as the values of "a" for each
    # process.
    monitor = Collector(('t', sim.now), get_objects(procs, 'pid', 'a'))
        
    # Run the simulation by using the band-new "peek()" and "step()" methods.
    while sim.peek() < 10:
        sim.step()
        monitor()

def storage_release_example():
    print 'Storage release example (this is really more of a test)'

    from collectors.core import DefaultStorage

    class YellingStorage(DefaultStorage):
        def __del__(self):
            print 'Oh noez, I wuz deleted'

    class ObserveMe(object):
        pass

    obj = ObserveMe()
    c = Collector(get(obj, 'value_a', 'value_b'), backend=YellingStorage())

    import gc
    gc.collect()

    print 'Collector initialized'

    for a, b in zip(range(10), reversed(range(10))):
        obj.value_a, obj.value_b = a, b
        c()

def pytables_example():
    import tables

    from collectors import storage

    class ObserveMe(object):
        a = 0
        b = 0

    obj = ObserveMe()
    h5file = tables.openFile('/tmp/example.h5', mode='w')
    collector = Collector(get(obj, 'a', 'b'),
            backend=storage.PyTables(h5file, 'groupname', ('int', 'int'))
    )

    for values in zip(range(10), reversed(range(10))):
        obj.a, obj.b = values
        collector()

    print collector.a.read(), collector.b.read()
    h5file.close()

def excel_example():
    from xlwt import Workbook
    from collectors import storage

    w = Workbook()
    s = w.add_sheet('my collected data')

    class ObserveMe(object):
        pass

    obj = ObserveMe()
    c = Collector(get(obj, 'value_a', 'value_b'), backend=storage.Excel(w, s))

    for a, b in zip(range(10), reversed(range(10))):
        obj.value_a, obj.value_b = a, b
        c()

    w.save('/tmp/example.xls')

if __name__ == '__main__':
    simpy_example()
    storage_release_example()
    pytables_example()
    excel_example()
