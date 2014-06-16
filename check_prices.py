#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notify via email when there are price drops on greek eshop's products.

Supported eshops:

    * www.skroutz.gr
    * www.bestprice.gr

"""

import urllib
import logging
import argparse

from utils import Configuration, setup_logging
from parsers import get_price
from email_servers import send_email


def parse_arguments():
    """ Parse command line arguments and return them as a namespace.  """

    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[1:2],
        prog=__file__,
        epilog="")

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='0.1.0'
    )

    parser.add_argument(
        '-c', '--config-file',
        action="store",
        dest="config_file",
        default="./check_prices.ini",
        help='Config file location. Defaults to "./check_prices.ini"',
    )

    options = parser.parse_args()

    # Initialize configuration
    config = Configuration()
    config.initialize(options.config_file)

    return options


def process(row):
    log = logging.getLogger("process")
    url, initial_price, percentage = row.split(",")
    initial_price = float(initial_price)
    percentage = float(percentage)
    try:
        current_price = get_price(url)
    except urllib.error.HTTPError:
        log.error("Wrong url. Please check the CSV.")
    else:
        delta = (initial_price - current_price) / initial_price * 100
        log.debug("Initial price: %.2f", initial_price)
        log.debug("Current price: %.2f", current_price)
        if delta > percentage:
            log.warning("The price did change significantly (%.2f%% > %.2f%%)", delta, percentage)
            send_email(url, initial_price, current_price, delta)
        else:
            log.info("The price has not changed significantly (%.2f%% < %.2f%%)", delta, percentage)


def main():
    """ main function. """
    # initialize things
    parse_arguments()
    setup_logging()
    config = Configuration()

    log = logging.getLogger("main")
    with open(config.input_file) as fd:
        log.info("Opening: %s", config.input_file)
        rows = fd.readlines()
        log.info("It contains %d rows", len(rows))

    for row in rows:
        process(row)


if __name__ == "__main__":
    main()
