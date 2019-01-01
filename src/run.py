# -*- coding:utf-8 -*-

"""
Created on  2019-01-01 17:03:03
@author: Xiaoyu Xie
@email: xiaoyuxie.vico@gmail.com
"""

import json
import sys
import traceback

from oss_uploader import Uploader
from utils import parser_args
from settings import UPDATE_SETTINGS, HELP_URL, OSS_INFO
from workflow import Workflow


def main(wf):
    args = parser_args(wf.args)
    if 'query' in args:
        image_name = args["query"]
        OSS_INFO['image_name'] = image_name

    uploader = Uploader(**OSS_INFO)

    if args["mode"] == "clipboard":
        results = uploader.upload()

    for ret in results:
        wf.add_item(
            title=ret['title'],
            subtitle=ret['subtitle'],
            valid=True,
            uid=ret['uid'],
            arg=ret['arg'],
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)
    sys.exit(wf.run(main))
