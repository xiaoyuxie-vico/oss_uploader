# -*- coding:utf-8 -*-

"""
Created on 2019-01-01 17:03:03
@author: Xiaoyu Xie
@email: xiaoyuxie.vico@gmail.com
"""


def parser_results(url):
    items_1 = {
        'title': 'Single url',
        'subtitle': 'Put image to OSS',
        'valid': True,
        'uid': url,
        'arg': url,
    }
    items_2 = {
        'title': 'Url in markdown format',
        'subtitle': 'Put image to OSS',
        'valid': True,
        'uid': url,
        'arg': '![]()'.format(url),
    }

    results = [items_1, items_2]
    return results


def parser_args(argv):
    """
    Parse Alfred Arguments
    """
    args = {}

    # determine search mode
    if(argv[0].lower() == "--clipboard"):
        args["mode"] = "clipboard"

    args["query"] = argv[1].lower()

    return args
