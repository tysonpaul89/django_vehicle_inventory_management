import sys
import traceback
import logging

class Utility(object):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    def get_logger(self):
        """Method return the logger instance"""
        return self.__logger

    @classmethod
    def get_exception(self):
        """Method get the detailed exception message"""
        cla, exc, trbk = sys.exc_info()
        exc_name = cla.__name__
        try:
            exc_args = exc.__dict__["args"]
        except KeyError:
            exc_args = "<no args>"
        exc_tb = traceback.format_tb(trbk, 8)
        message = '%s %s %s' % (exc_name, exc_args, exc_tb)
        return message