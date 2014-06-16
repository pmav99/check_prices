#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
parsers
"""

from .skroutz import get_price as get_price_skroutz
from .bestprice import get_price as get_price_best_price


__all__ = ["get_price"]


def get_price(url):
    if "skroutz" in url:
        function = get_price_skroutz
    elif "best_price.gr" in url:
        function = get_price_best_price
    else:
        raise Exception("Unkown website. Please write a parser")

    return function(url)
