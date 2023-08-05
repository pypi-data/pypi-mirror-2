from pymongo import Connection, DESCENDING
from time import time, strftime, gmtime
from waskr.util import config_options

class WaskrStats(object):

    def __init__(self,config=None):
        if config == None:
            config = config_options()
        self.conn = Connection(
                config['db_host'], 
                config['db_port'])
        self.db_waskr = self.conn['waskr']
        self.db = self.db_waskr['stats']


    def last_insert(self):
        last = self.db.find().sort('time', DESCENDING).limit(1)
        for entry in last:
            unix_time =  entry['time']
            struct = gmtime(unix_time)
            formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
            return formatted


    def apps_nodes(self):
        apps = []
        for application in self.db.distinct('application'):
            c = self.db.find({'application':application})
            for record in c:
                match = (record['application']), record['server_id']
                if match not in apps:
                    apps.append(match)
        return apps


    def response_time(self, minutes):
        """Get the last N minutes of response stats"""
        time_response = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        print "start %d " % start
        records = self.db.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            data = []
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(stat['response'])
            time_response.append(data)
        return time_response


    def request_time(self, minutes):
        """Get the last N minutes of request stats"""
        requests_second = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.db.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            data = []
            hits = self.db.find({'time':stat['time']}).count()
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(hits)
            requests_second.append(data)
        return requests_second

