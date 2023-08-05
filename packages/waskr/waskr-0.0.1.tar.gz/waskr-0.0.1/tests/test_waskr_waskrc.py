import unittest
from subprocess import Popen, PIPE


class TestMain(unittest.TestCase):


    def test_help(self):
        argument = 'waskrc --help'
        run = Popen(argument, shell=True, stdout=PIPE)
        actual = [i for i in run.stdout.readlines()]
        expected = ['Usage: waskrc [options]\n', '\n', 
                'WASKR Command Line Utility\n', '\n', 'Options:\n', 
                "  --version        show program's version number and exit\n", 
                '  -h, --help       show this help message and exit\n', 
                '  --server=SERVER  Runs the web server.  If no configuration file is passed\n', 
                '                   localhost and port 8080 is used.\n']
        self.assertEqual(expected, actual)


    def test_no_args(self):
        argument = 'waskrc'
        run = Popen(argument, shell=True, stdout=PIPE)
        actual = [i for i in run.stdout.readlines()]
        expected = ['Usage: waskrc [options]\n', '\n', 
                'WASKR Command Line Utility\n', '\n', 'Options:\n', 
                "  --version        show program's version number and exit\n", 
                '  -h, --help       show this help message and exit\n', 
                '  --server=SERVER  Runs the web server.  If no configuration file is passed\n', 
                '                   localhost and port 8080 is used.\n']
        self.assertEqual(expected, actual)


    def test_server_no_arg(self):
        argument = 'waskrc --server'
        run = Popen(argument, shell=True, stderr=PIPE)
        actual = [i for i in run.stderr.readlines()]
        expected = ['Usage: waskrc [options]\n', 
                '\n', 
                'waskrc: error: --server option requires an argument\n'] 
        self.assertEqual(expected, actual)

    def test_server_bad_arg(self):
        argument = 'waskrc --server foobar'
        run = Popen(argument, shell=True, stderr=PIPE, stdout=PIPE)
        actual = [i for i in run.stderr.readlines()]
        expected = 'No valid file provided'
        self.assertEqual(expected, actual[0])


if __name__ == '__main__':
    unittest.main()
