import unittest
from os import remove

from waskr import config_options 

def setup():
    txt = open('conf.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s
    """
    txt.write(text)
    txt.close()

    txt = open('conf_two.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()

    txt = open('conf_three.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()

    txt = open('conf_four.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()

    txt = open('conf_five.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()

    txt = open('conf_six.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()

    txt = open('conf_seven.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname) [%(name)s]  %(message)s    
"""
    txt.write(text)
    txt.close()


def teardown():
    remove('conf.ini') 
    remove('conf_two.ini') 
    remove('conf_three.ini') 
    remove('conf_four.ini') 
    remove('conf_five.ini') 
    remove('conf_six.ini') 
    remove('conf_seven.ini') 



class TestConfigOptions(unittest.TestCase):

    def setUp(self):
        self.opt_mapper = {
            'waskr.db.host':'db_host',
            'waskr.db.port':'db_port',
            'waskr.web.host':'web_host',
            'waskr.web.port':'web_port',
            'waskr.middleware.application':'application',
            'waskr.middleware.server_id':'server_id',
            'waskr.log.level':'log_level',
            'waskr.log.format':'log_format',
            'waskr.log.datefmt':'log_datefmt'
            }

        self.defaults = {
            'server_id': '1',
            'db_host': 'localhost',
            'db_port': 27017,
            'application': 'main',
            'web_host': 'localhost',
            'web_port': '8080',
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }


    def test_config_options_TypeError(self):
        actual = config_options(config={})
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_config_options_empty(self):
        actual = config_options()
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_config_options_invalid_file(self):
        actual = config_options('/path/to/invalid/file.txt')
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_config_options_typeError(self):
        actual = config_options(['a list should never be passed'])
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_config_options_Error_string(self):
        actual = config_options('a string should never be passed')
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_config_options_ini(self):
        actual = config_options('conf.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_no_id(self):
        actual = config_options('conf_two.ini')
        expected = { 
                'server_id': '1',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_no_dbhost(self):
        actual = config_options('conf_three.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'localhost',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_no_dbport(self):
        actual = config_options('conf_four.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': 27017,
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_noapp(self):
        actual = config_options('conf_five.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'main',
                'web_host': 'web.example.com',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_no_webhost(self):
        actual = config_options('conf_six.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'localhost',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_config_options_ini_no_webport(self):
        actual = config_options('conf_seven.ini')
        expected = { 
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '8080',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
