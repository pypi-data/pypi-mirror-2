#!/usr/bin/env python

""" WASKR Command Line Utility """

__version__ = '0.0.2'

from optparse import OptionParser
from os import path
import sys

from waskr.web import server
from waskr import config_options

def main():
    """Handle all options"""
    parser = OptionParser(description="""WASKR Command Line Utility""", 
            version=__version__)
    parser.add_option('--server', action='store_true', help="""Runs the web server. 
If no configuration file is passed localhost and port 8080 is used.""")
    parser.add_option('--conf', help="""Pass a INI configuration file""")

    options, arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()


    if options.server:
        if options.conf and path.isfile(options.conf):
            configuration = config_options(options.conf)
            server.CONF = configuration
            server.main(configuration)
        else:
            server.main()


if __name__ == "__main__":
        main() 
