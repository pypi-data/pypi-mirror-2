import unittest
from subprocess import Popen, PIPE


class TestMain(unittest.TestCase):


    def test_help(self):
        argument = 'waskrc --help'
        actual = Popen(argument, stdout=PIPE, shell=True).communicate()[0]
        expected = "Usage: waskrc [options]\n\nWASKR Command Line Utility\n\nOptions:\n  --version             show program's version number and exit\n  -h, --help            show this help message and exit\n  --server              Runs the web server.  If no configuration file is\n                        passed localhost and port 8080 is used.\n  --conf=CONF           Pass a INI configuration file\n  --add-user=ADD_USER   Adds a user email for the web interface\n  --remove-user=REMOVE_USER\n                        Removes a user email from the web interface\n"
        self.assertEqual(expected, actual)


    def test_no_args(self):
        argument = 'waskrc'
        actual = Popen(argument, shell=True, stdout=PIPE).communicate()[0]
        expected = "Usage: waskrc [options]\n\nWASKR Command Line Utility\n\nOptions:\n  --version             show program's version number and exit\n  -h, --help            show this help message and exit\n  --server              Runs the web server.  If no configuration file is\n                        passed localhost and port 8080 is used.\n  --conf=CONF           Pass a INI configuration file\n  --add-user=ADD_USER   Adds a user email for the web interface\n  --remove-user=REMOVE_USER\n                        Removes a user email from the web interface\n"
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
