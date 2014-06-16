#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
skroutz.gr parser
"""

import re

from utils import get_page


PATTERN = re.compile(
    r"(?:lowPrice\">)"           # the opening <span>
    r"(\d+[\.|,]\d{2})"          # the actual price
    r"(?:"
        r"\s{0,1}"               # optionally a space between price and currency
        r".+"                    # the currency symbol
        r"<\/span>"              # the closing <\span>
    r")",
    re.MULTILINE)


def get_price(url):
    """ Return the price """
    # retrieve data
    page = get_page(url)
    result = PATTERN.search(page)
    price = result.groups()[0]
    print(price)
    # fix data
    price = float(price.replace(",", "."))
    return price
