import unittest

"""Make sure we are able to import everything from waskr"""


class TestImports(unittest.TestCase):

    def test_import_waskr(self):
        try:
            import waskr
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_database(self):
        try:
            from  waskr import database
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_middleware(self):
        try:
            from waskr import middleware
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_RequestStatsMiddleware(self):
        try:
            from waskr.middleware import RequestStatsMiddleware
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_util(self):
        try:
            from waskr import util
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_web(self):
        try:
            from waskr import web
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_server(self):
        try:
            from waskr.web import server
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_model(self):
        try:
            from waskr.web  import model
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_model_WaskStats(self):
        try:
            from waskr.web.model  import WaskrStats
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_session_Authentication(self):
        try:
            from waskr.web.session  import Authentication
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_session(self):
        try:
            from waskr.web  import session
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_db_stats(self):
        try:
            from waskr.database  import Stats
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_Synchronizer(self):
        try:
            from waskr.util  import Synchronizer
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_RequestParser(self):
        try:
            from waskr.util  import Synchronizer
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_config_options(self):
        try:
            from waskr.util  import config_options
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_util_config_defaults(self):
        try:
            from waskr.util  import config_defaults
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)



if __name__ == '__main__':
    unittest.main()
