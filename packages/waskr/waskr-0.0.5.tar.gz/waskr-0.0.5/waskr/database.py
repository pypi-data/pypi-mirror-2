from pymongo import Connection, DESCENDING
from time import time, strftime, gmtime
from waskr import config_options
import log

class Stats(object):

    def __init__(self, config=None, test=False):
        if config == None:
            config = config_options()
        self.connection = Connection(
                config['db_host'], 
                int(config['db_port']))
        self.waskr = self.connection['waskr']
        self.stats = self.waskr['stats']
        self.users = self.waskr['user']
        log.database.debug("database connection initialized")
        if test:
            self.waskr = self.connection['test_waskr']
            self.stats = self.waskr['stats']
            self.users = self.waskr['user']

    def insert(self, stats):
        # Stats should come as a list of dictionaries
        for stat in stats:
            self.stats.insert(stat)
        log.database.debug("inserted stats to database")

    def last_insert(self):
        last = self.stats.find().sort('time', DESCENDING).limit(1)
        for entry in last:
            unix_time =  entry['time']
            struct = gmtime(unix_time)
            formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
            return formatted
        log.model.debug("returned formatted last insert from database")

    def apps_nodes(self):
        apps = []
        for application in self.stats.distinct('application'):
            c = self.stats.find({'application':application})
            for record in c:
                match = (record['application']), record['server_id']
                if match not in apps:
                    apps.append(match)
        return apps
        log.model.debug("returned all application nodes present")

    def response_time(self, minutes):
        """Get the last N minutes of response stats"""
        time_response = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.stats.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            data = []
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(stat['response'])
            time_response.append(data)
        log.model.debug("returned the last N minutes of response stats")
        return time_response

    def request_time(self, minutes):
        """Get the last N minutes of request stats"""
        requests_second = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.stats.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            data = []
            hits = self.stats.find({'time':stat['time']}).count()
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(hits)
            requests_second.append(data)
        return requests_second
        log.model.debug("returned requests per second")
    
    def first_run(self, manual_email=None):
        """A first run is True when no user email has been set"""
        if self.have_user():
            pass
        else:
            if manual_email:
                self.add_user(manual_email)
                log.model.info("adding new user email")
  
            if not manual_email:
                add_email = raw_input("""
Seems this is the first time you are running the waskr
we application..
You need to set an email to access the web interface.
Email: """)
                if not add_email:
                    add_email # we ask again
                    log.model.error("user did not supply email - asking again")
                else:
                    self.add_user(add_email)
            
    def have_user(self):
        try:
            for i in self.users.find_one():
                if i:
                    return True
                    log.model.debug("found valid user - returning True")
        except:
            return False
            log.model.info("no valid user found - returning False")

    def remove_user(self, email):
        new_user = {'email':email}
        self.users.remove(new_user)

    def add_user(self, email):
        new_user = {'email':email}
        self.users.insert(new_user)

    def authenticate(self, email):
        try:
            for user_email in self.users.find({'email':email}):
                if user_email['email'] == email:
                    return True
                    log.model.info("found authorized user with matching email")
                else:
                    return False
        except:
            return False
            log.model.info("user not authorized - no matching email found")
