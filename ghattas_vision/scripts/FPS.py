import time

class FPS(object):
    def __init__(self):
        self.last_time = time.time()

    def update(self):
        period = time.time()-self.last_time
        print('Loop took {} seconds'.format(period))
        print('FPS = {}'.format(1/period))
        self.last_time = time.time()
