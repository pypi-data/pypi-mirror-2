import logging



class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("twisted.scheduling").addHandler(NullHandler())
