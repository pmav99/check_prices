#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notify via email.

"""

import argparse

from utils import Configuration
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
    url, initial_price, percentage = row.split(",")
    initial_price = float(initial_price)
    percentage = float(percentage) / 100
    current_price = get_price(url)
    delta = (initial_price - current_price) / initial_price
    if delta > percentage:
        send_email(url, initial_price, current_price, delta)
    else:
        print("Small change")


def main():
    """ main function. """
    parse_arguments()
    config = Configuration()

    with open(config.input_file) as fd:
        data = fd.readlines()

    for row in data:
        process(row)

if __name__ == "__main__":
    main()
