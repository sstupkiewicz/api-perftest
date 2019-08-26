from logging import getLogger, FileHandler, Formatter, DEBUG, INFO
from argparse import ArgumentParser, FileType
from datetime import datetime
from os.path import isfile
from configparser import RawConfigParser
from time import sleep

import requests
import threading
from lib.Test import Test
import json

def initiate_logging(logger_name, logfile, level=INFO):
    '''
    Returns configured logging instance to use for logging and debugging.

    logger_name: Custom name that serves as differentiator of different logging instances
    logfile: Name of a file that logger will write to by default
    level: Log level that will be used in the script. WARNING: DEBUG level will write plain-text password into logfile!
    '''
    logger = getLogger(logger_name)
    logger.setLevel(level)
    formatter = Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
    file_handler = FileHandler(logfile, 'a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def parse_arguments(description):
    parser = ArgumentParser(description)
    parser.add_argument('-i', '--id', type=str, help="Client id.")
    parser.add_argument('-u', '--url', type=str, help="URL to call")
    parser.add_argument('-t', '--threads', type=int, default=2 ,help="Threads to run. Defaults to 2.")
    parser.add_argument('-b', '--bursts', type=int, default=2 ,help="Bursts to run. Defaults to 2.")
    arguments = parser.parse_args()
    return arguments

def main():

    options = parse_arguments("API Load generator")
    if options.id == None or options.url == None:
        print("You need to pass additional arguments. Please use --help to display available options.")
    else:
        t = Test(options.url, options.id, options.bursts, options.threads )
        t.run()
    return 0

if __name__ == "__main__":
    exit(main()) 