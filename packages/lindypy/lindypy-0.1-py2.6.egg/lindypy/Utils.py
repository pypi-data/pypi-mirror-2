"""
Some utilities to make programming with tuple spaces
easier.
"""
import os
import signal
import multiprocessing

class TimeoutError(Exception): pass

class timeout(object):

    def __init__(self, seconds):
        self.seconds = seconds
        self.boom = False

    def __enter__(self):
        self.oldsig = signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM, self.bailout)
        signal.alarm(self.seconds)

    def __exit__(self, *args):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.oldsig)
        if self.boom:
            raise TimeoutError("timed out")

    def bailout(self, *args):
        self.boom = True

