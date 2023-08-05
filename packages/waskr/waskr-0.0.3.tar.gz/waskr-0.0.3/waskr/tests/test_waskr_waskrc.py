import unittest
from subprocess import Popen, PIPE


class TestMain(unittest.TestCase):


    def test_help(self):
        argument = 'waskrc --help'
        actual = Popen(argument, stdout=PIPE, shell=True).communicate()[0]
        expected = """Usage: waskrc [options]\n\nWASKR Command Line Utility\n\nOptions:\n  --version    show program's version number and exit\n  -h, --help   show this help message and exit\n  --server     Runs the web server.  If no configuration file is passed\n               localhost and port 8080 is used.\n  --conf=CONF  Pass a INI configuration file\n"""

        self.assertEqual(expected, actual)


    def test_no_args(self):
        argument = 'waskrc'
        actual = Popen(argument, shell=True, stdout=PIPE).communicate()[0]
        expected = """Usage: waskrc [options]\n\nWASKR Command Line Utility\n\nOptions:\n  --version    show program's version number and exit\n  -h, --help   show this help message and exit\n  --server     Runs the web server.  If no configuration file is passed\n               localhost and port 8080 is used.\n  --conf=CONF  Pass a INI configuration file\n"""
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
