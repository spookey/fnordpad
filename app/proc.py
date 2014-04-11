'''little man with a clock in his pocket'''

from multiprocessing import Process, Pool
from threading import Timer
from app.log import LOGGER

class Cycle(object):
    '''tick tock'''

    def __init__(self, interval, function, *args, **kwargs):
        super().__init__()
        self._interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        LOGGER.info('new cycle created %s (%s seconds)' %(self.function.__name__, self._interval))

    def _run(self):
        if self.is_running:
            LOGGER.info('cycle tick %s (%s seconds)' %(self.function.__name__, self._interval))
            p = Process(target=self.function, args=self.args, kwargs=self.kwargs)
            p.start()
            p.join()
            Timer(self._interval, self.start).start()
        self.is_running = False

    def start(self):
        self.is_running = True
        LOGGER.info('cycle started %s (%s seconds)' %(self.function.__name__, self._interval))
        self._run()


    def stop(self):
        self.is_running = False
        LOGGER.info('cycle stopped %s (%s seconds)' %(self.function.__name__, self._interval))

def tpool(function, data):
    LOGGER.info('new tpool %s - %s' %(function.__name__, data))
    pool = Pool()
    pool.map(function, data)
    pool.close()
    pool.join()

