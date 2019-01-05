# -*- coding:utf-8 -*-

"""
Created on 2019-01-01 17:03:03
@author: Xiaoyu Xie
@email: xiaoyuxie.vico@gmail.com
"""

import tinify
import traceback


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


def compress_image(image_path, out_path, key):
    """
    Compress the local image, return saved_image (local path)
    """
    tinify.key = key
    try:
        source = tinify.from_file(image_path)
        source.to_file(out_path)
        return out_path
    except:
        traceback.print_exc()
        return False
