# -*- coding:utf-8 -*-

"""
Created on 2018-12-31 18:11:59
@author: Xiaoyu Xie
@email: xiaoyuxie.vico@gmail.com
"""

import os
import time

import oss2
import json
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSFilenamesPboardType


class Uploader(object):
    """
    uploader for Ali oss on python2.7
    """

    def __init__(self, **kargs):
        self.access_key_id = kargs.get('access_key_id', None)
        self.access_key_secret = kargs.get('access_key_secret', None)
        self.bucket_name = kargs.get('bucket_name', None)
        self.endpoint = kargs.get('endpoint', None)

    def connect(self):
        """
        oss connect
        """
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    @staticmethod
    def save_clipboard_data():
        """
        save clipboard data to local umage
        """
        pb = NSPasteboard.generalPasteboard()
        data_type = pb.types()

        if NSPasteboardTypePNG in data_type:
            data = pb.dataForType_(NSPasteboardTypePNG)
            # using time to name the image
            file_name = '{}.png'.format(int(time.time()))
            file_path = os.path.join('/tmp', file_name)
            ret = data.writeToFile_atomically_(file_path, False)
            # if save right return file_path
            if ret:
                return file_path
        elif NSFilenamesPboardType in data_type:
            # file in machine
            return pb.propertyListForType_(NSFilenamesPboardType)[0]

    @staticmethod
    def parser_image_name(image_name):
        """
        save image in oss based on date, return image_path in oss
        Example: save images on oss based on time
        """
        date = time.strftime("%Y-%m-%d", time.localtime())
        image_path_oss = os.path.join(date, image_name)
        return image_path_oss

    @staticmethod
    def parser_url_result(url):
        """
        parser url result for Alfred
        """
        data = {
            'items': [
                {'title': 'Single url', 'arg': url, "icon":
                    {
                        'type': 'png',
                        'path': 'icon.png'
                    }
                 },
                {'title': 'Url for markdown', 'arg': '![](%s)' % url, 'icon':
                    {
                        'type': 'png',
                        'path': 'icon.png'
                    }
                 }
            ]
        }
        url_result = json.dumps(data)
        return url_result

    def upload(self, image_path_local=None):
        """
        upload image to Ali oss
        """
        self.connect()

        # get image path
        if not image_path_local:
            image_path_local = self.save_clipboard_data()
        image_name = os.path.basename(image_path_local)
        image_path_oss = self.parser_image_name(image_name)

        # upload to oss
        result = self.bucket.put_object_from_file(
            image_path_oss, image_path_local)

        url = result.resp.response.url
        url_result = self.parser_url_result(url)
        print(url_result)


if __name__ == '__main__':
    kargs = {
        'access_key_id': '<你的AccessKeyId>',
        'access_key_secret': '<你的AccessKeySecret>',
        'bucket_name': '<你的Bucket名>',
        'endpoint': 'http://oss-cn-hangzhou.aliyuncs.com',  # example
    }
    uploader = Uploader(**kargs)
    uploader.upload()
