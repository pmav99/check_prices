#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

__all__ = ["send_email"]

from email.utils import formataddr
from email.mime.text import MIMEText

from utils import Configuration
from .gmx import get_server as get_server_gmx
from .gmail import get_server as get_server_gmail


GET_SERVER_FUNCTIONS = {
    "gmail.com": get_server_gmail,
    "gmx.com": get_server_gmx,
}

MESSAGE_TEMPLATE =\
"""
Προϊόν       : {url}
Αρχική τιμή  : {initial_price}
Τρέχουσα τιμή: {current_price}
Μεταβολή     : {delta} \%
"""

def get_message(url, initial_price, current_price, delta):
    """ Return the email message (body + headers). """
    config = Configuration()

    message = MESSAGE_TEMPLATE.format(
        url=url,
        initial_price=initial_price,
        current_price=current_price,
        delta=delta)

    # create the actual email message
    msg = MIMEText(message)
    msg['To'] = formataddr(('Recipient', config.recipients))
    msg['From'] = formataddr(('Author', config.username))
    msg['Subject'] = 'Προσφορά'

    return msg


def send_email(url, initial_price, current_price, delta):
    """ Send the given `msg` using the given `server`. """
    # read values from configuration
    config = Configuration()
    username = config.username
    password = config.password
    recipients = config.recipients
    provider = username.split("@")[1]       # determine the email provider by parsing the username
    get_server = GET_SERVER_FUNCTIONS[provider]
    server = get_server(username, password)
    msg = get_message(url, initial_price, current_price, delta)

    try:
        server.sendmail(username, recipients, msg.as_string())
    finally:
        server.quit()

