#!/usr/bin/env python

""" WASKR Command Line Utility """

__version__ = '0.0.1'

from optparse import OptionParser
from os import path
import sys

from waskr.web import server
from waskr.util import config_options

def main():
    """Handle all options"""
    parser = OptionParser(description="""WASKR Command Line Utility""", 
            version=__version__)
    parser.add_option('--server', help="""Runs the web server. 
If no configuration file is passed localhost and port 8080 is used.""")

    options, arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if options.server:
        if path.isfile(options.server):
            configuration = config_options(options.server)
            server.CONF = configuration
            server.main(options.server)
        else:
            sys.stderr.write('No valid file provided')
            sys.exit(1)

if __name__ == "__main__":
        main() 
