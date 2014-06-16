#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
various utilities
"""

import os
from urllib.request import urlopen
from email.utils import formataddr
from email.mime.text import MIMEText
from configparser import ConfigParser


__all__ = ["Configuration", "get_page"]


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
        parser = ConfigParser()
        parser.read(os.path.realpath(config_file))

        self.username = parser.get("email", "username")
        self.password = parser.get("email", "password")
        self.recipients = parser.get("email", "recipients")
        self.input_file = parser.get("general", "input_file")


def get_page(url):
    """ Return the response of the given `url` as a string. """
    response = urlopen(url)
    response_code = response.getcode()
    if response_code == '404':
        raise Exception("Wrong Link")
    text = response.read().decode('utf8')
    return text



