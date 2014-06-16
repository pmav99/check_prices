#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parsers
"""

import logging

from .skroutz import get_price as get_price_skroutz
from .bestprice import get_price as get_price_best_price


__all__ = ["get_price"]


def get_price(url):
    """ Return the price of the product. """
    log = logging.getLogger("parsers")
    log.info("Querying: %s", url)
    if "skroutz" in url:
        log.debug("This is a skroutz.gr link.")
        function = get_price_skroutz
    elif "bestprice.gr" in url:
        log.debug("This is a bestprice.gr link.")
        function = get_price_best_price
    else:
        raise Exception("Unkown website. Please write a suitable parser")

    return function(url)
