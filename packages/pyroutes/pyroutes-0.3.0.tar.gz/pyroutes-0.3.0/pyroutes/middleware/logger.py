import logging

class LoggingMiddleware(object):
    def __init__(self, passthrough):
        self.logger = logging.getLogger('pyroutes')
        self.logger.addHandler(logging.FileHandler('/tmp/foologger.txt'))
        self.logger.setLevel(logging.DEBUG)
        self.passthrough = passthrough

    def __call__(self, request):
        self.logger.debug('Got request %s', request)
        response = self.passthrough(request)
        self.logger.debug('Got response %s', response)
        return response

