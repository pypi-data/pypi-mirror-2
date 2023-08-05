import unittest
from time import time

from waskr.middleware import RequestStatsMiddleware


class TestRequestStatsMiddleware(unittest.TestCase):


    def test_timing(self):
        """Timing substracts zero from current time"""
        application = RequestStatsMiddleware(app=None)
        actual = int(application.timing(zero=0))
        expected = int(time())
        self.assertEqual(actual, expected)

    def test_config(self):
        """Config should be defaults if None is passed"""
        application = RequestStatsMiddleware(app=None)
        actual = application.config 
        expected = {
                'server_id': '1', 
                'web_port': '8080', 
                'db_port': 27017, 
                'application': 'main', 
                'db_host': 'localhost', 
                'web_host': 'localhost',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname) [%(name)s]  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
