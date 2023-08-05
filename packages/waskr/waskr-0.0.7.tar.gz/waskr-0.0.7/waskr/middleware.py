from time import time
from waskr import config_options, setlogging
from util import RequestParser
import log

class RequestStatsMiddleware(object):

    def __init__(self, app, config=None):
        """Initialize the RequestStats Middleware
        Every single request will get logged with a unix timestamp
        the time it took to respond and the url that was requested.
        The dictionary is passed on the RequestParser that deals
        with building the cache and submitting the data to 
        the queue.
        """
        self.app = app

        log.middleware.debug('Middleware Initialized')
        self.config = config_options(config)
        self.parser = RequestParser(self.config)

        setlogging(self.config)

    def __call__(self, environ, start_response):
        zero = time()
        data = {}
        try:
            return self.app(environ, start_response)
        finally:
            data['time']        = int(time())
            data['response']    = self.timing(zero)
            data['url']         = environ['PATH_INFO']
            data['server_id']   = self.config['server_id']
            data['application'] = self.config['application']
            self.parser.construct(data)             
    
    def timing(self, zero):
        log.middleware.debug('returning time object')
        return time() - zero

