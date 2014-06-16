#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
various utilities
"""

import os
import logging
import urllib
from urllib.request import urlopen
from email.utils import formataddr
from email.mime.text import MIMEText
from configparser import ConfigParser


__all__ = ["Configuration", "get_page", "setup_logging"]


class Borg(object):
    """ A class which "shares state" among its instances. """
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state


class Configuration(Borg):
    """
    Global configuration class.

    This is a subclass of Borg. It can only be initialized only once.
    """

    def initialize(self, config_file):
        """ Should only be called once. """
        parser = ConfigParser()
        parser.read(os.path.realpath(config_file))

        self.username = parser.get("email", "username")
        self.password = parser.get("email", "password")
        self.recipients = [line for line in parser.get("email", "recipients").splitlines() if line]
        self.input_file = parser.get("general", "input_file")


def get_page(url):
    """ Return the response of the given `url` as a string. """
    response = urlopen(url)
    response_code = response.getcode()
    text = response.read().decode('utf8')
    return text



def setup_logging():
    """ setup logging. """
    # initialize the root logger
    logger = logging.getLogger()
    logger.setLevel(0)  # Yes, this is necessary! I think it has to do with propagate etc

    # Create the formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s; %(levelname)-8s; %(name)-15s; %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    # add the handlers to logger
    logger.addHandler(console_handler)
