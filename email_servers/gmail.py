#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

import smtplib

SERVER = 'smtp.gmail.com'
PORT = 587


def get_server(username, password):
    """ Return a server for gmx.com. """
    server = smtplib.SMTP(SERVER, PORT)
    server.login(username, password)
    return server
