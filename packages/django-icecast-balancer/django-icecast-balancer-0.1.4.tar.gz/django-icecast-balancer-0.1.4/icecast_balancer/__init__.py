'''
Simple HTTP based load-balancer for IceCast2.
Created on 28.12.2009
For licensing see COPYING.
'''
import os
import logging

VERSION = (0,1,4)
__version__ = '.'.join(map(str, VERSION))

class Logging(object):
    """ 
    A private class that loads and caches some global objects.
    """
    logger = None

    def get_logger(cls):
        """ 
        Initializes and returns our logger instance.
        """
        if cls.logger is None:
            class NullHandler(logging.Handler):
                def emit(self, record):
                    pass

            cls.logger = logging.getLogger('icecast_balancer')
            cls.logger.addHandler(NullHandler())
            cls.logger.setLevel(logging.DEBUG)

        return cls.logger
    get_logger = classmethod(get_logger)
