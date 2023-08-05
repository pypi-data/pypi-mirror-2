"""Runs a thread that looks for stuff to sync in a queue that is
shared accross the middleware for efficient/low-overhead performance"""

from ConfigParser import ConfigParser
from os.path import isfile
from threading import Thread
import Queue

from database import Stats


class Synchronizer(Thread):
    """Checks the queue every n minutes and pushes
    the data to the database if it finds an item"""

    def __init__(self, queue, config):
        self.config = config
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            stats = self.queue.get()
            self.push_to_db(stats)
            self.queue.task_done()

    def push_to_db(self, stats):
        db = Stats(self.config) 
        db.insert(stats)


class RequestParser(object):
    """Receives a dictionary with the request and arranges
    the data to pass to the Queue instance"""

    def __init__(self, config):
        self.config = config
        self.queue = Queue.Queue()
        self.cache = []
        self.spawn_sync()

    def construct(self, data):
        self.cache.append(data)
        if len(self.cache) == 10:
            self.push_to_queue(self.cache)
            self.flush()

    def flush(self):
        """Flushes the cached data after it goes to the 
        Queue"""
        self.cache = []

    def push_to_queue(self, stats):
        """Submits a dictionary of stats to the queue"""
        self.queue.put(stats)

    def spawn_sync(self):
        """Creates a thread that will fetch data from the queue"""
        sync = Synchronizer(self.queue, self.config)
        sync.setDaemon(True)
        sync.start()


def config_options(config=None):
    """Instead of calling ConfigParser all over the place
    we gather, read, parse and return valid configuration
    values for any waskr utility here, config should
    always be a file object or None and config_options
    always returns a dictionary with values"""

    # If all fails we will always have default values
    configuration = config_defaults()

    # Options comming from the config file have
    # longer names, hence the need to map them correctly
    opt_mapper = {
            'waskr.db.host':'db_host',
            'waskr.db.port':'db_port',
            'waskr.web.host':'web_host',
            'waskr.web.port':'web_port',
            'waskr.middleware.application':'application',
            'waskr.middleware.server_id':'server_id'
            }

    try:
        if config == None or isfile(config) == False:
            configuration = config_defaults()
    except TypeError:
        if type(config) is dict:
            configuration = config_defaults(config)
    else:
        try:
            converted_opts = {}
            parser  = ConfigParser()
            parser.read(config)

            file_options = parser.defaults()

            # we are not sure about the section so we 
            # read the whole thing and loop through the items
            for key, value in opt_mapper.items():
                try:
                    file_value = file_options[key] # if this is true, we continue and means that KEY is valid
                    converted_opts[value] = file_value

                except KeyError:
                    pass # we will fill any empty values later with config_defaults
            configuration = config_defaults(converted_opts)
        except Exception:
            pass # TODO Implement the logging to catch these Exceptions

    return configuration
    

def config_defaults(config=None):
    """From the config dictionary it checks missing values and
    adds the defaul ones for them if any"""
    if config == None:
        config = {}
    defaults = {
            'server_id': '1',
            'db_host': 'localhost',
            'db_port': 27017,
            'application': 'main',
            'web_host': 'localhost',
            'web_port': '8080'
            }

    for key in defaults:
        try:
            config[key]
        except KeyError:
            config[key] = defaults[key]

    return config
