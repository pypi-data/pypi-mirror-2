from pymongo import Connection

class Authentication(object):

    def __init__(self):
            self.conn = Connection() # we need to get config options
            self.db_waskr = self.conn['waskr']
            self.users = self.db_waskr['user']
    
    def first_run(self):
        """A first run is True when no user email has been set"""
        if self.have_user():
            pass
        else:
            add_email = raw_input("""
Seems this is the first time you are running the waskr
we application..
You need to set an email to access the web interface.
Email: """)
            if add_email:
                self.add_user(add_email)
            else:
                add_email
            
    def have_user(self):
        try:
            for i in self.users.find_one():
                if i:
                    return True
        except:
            return False

    def add_user(self, email):
        new_user = {'email':email}
        self.users.insert(new_user)

    def authenticate(self, email):
        try:
            for user_email in self.users.find({'email':email}):
                if user_email['email'] == email:
                    return True
                else:
                    return False
        except:
            return False
