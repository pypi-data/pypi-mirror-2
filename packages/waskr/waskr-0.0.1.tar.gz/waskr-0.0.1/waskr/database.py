from pymongo import Connection, DESCENDING

class Stats(object):

    def __init__(self, config=None):
        self.connection = Connection(
                config['db_host'], 
                config['db_port'])
        self.waskr = self.connection['waskr']
        self.collection = self.waskr['stats']

    def insert(self, stats):
        # Stats should come as a list of dictionaries
        for stat in stats:
            self.collection.insert(stat)

    def last_insert(self):
        last = self.collection.find().sort('time', DESCENDING).limit(1)
        for entry in last:
            return entry
