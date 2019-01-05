# -*- coding:utf-8 -*-

"""
Created on  2019-01-01 17:03:03
@author: Xiaoyu Xie
@email: xiaoyuxie.vico@gmail.com
"""

import os
import time

import oss2
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSFilenamesPboardType

from settings_self import TINIFY_KEY
from utils import compress_image


class Uploader(object):
    """
    uploader for Ali oss on python2.7
    """

    def __init__(self, **kargs):
        self.access_key_id = kargs.get('access_key_id', None)
        self.access_key_secret = kargs.get('access_key_secret', None)
        self.bucket_name = kargs.get('bucket_name', None)
        self.endpoint = kargs.get('endpoint', None)
        # default to compress the image
        self.is_compress = kargs.get('is_compress', True)
        if kargs.get('image_name'):
            self.image_name = '{}.jpg'.format(kargs['image_name'])
        else:
            self.image_name = '{}.jpg'.format(int(time.time()))

    def connect(self):
        """
        oss connect
        """
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    @staticmethod
    def save_clipboard_data(image_name):
        """
        save clipboard data to local umage
        """
        pb = NSPasteboard.generalPasteboard()
        data_type = pb.types()

        if NSPasteboardTypePNG in data_type:
            data = pb.dataForType_(NSPasteboardTypePNG)
            image_path_uncompress = os.path.join('/tmp', 'temp_' + image_name)
            ret = data.writeToFile_atomically_(image_path_uncompress, False)

            image_path_compress = os.path.join('/tmp', image_name)
            # compress image
            compress_image(image_path_uncompress,
                           image_path_compress, TINIFY_KEY)

            # if save right return image_path_compress
            if ret:
                return image_path_compress
        elif NSFilenamesPboardType in data_type:
            # file in machine
            return pb.propertyListForType_(NSFilenamesPboardType)[0]

    @staticmethod
    def parser_path_in_oss(image_name):
        """
        save image in oss based on date, return image_path in oss
        Example: save images on oss based on time
        """
        date = time.strftime("%Y-%m-%d", time.localtime())
        image_path_oss = os.path.join(date, image_name)
        return image_path_oss

    @staticmethod
    def parser_results(url):
        """
        parse results for workflow
        """
        base = {
            "icon": {
                'type': 'png',
                'path': 'icon.png'
            }
        }

        items_1 = {
            'title': 'Single url',
            'subtitle': 'Upload',
            'valid': True,
            'uid': url,
            'arg': url,
        }
        items_2 = {
            'title': 'Url in markdown format',
            'subtitle': 'Upload',
            'valid': True,
            'uid': url,
            'arg': '![]({})'.format(url),
        }

        for item in [items_1, items_2]:
            item.update(base)

        results = [items_1, items_2]
        return results

    def upload(self, image_path_local=None):
        """
        upload image to Ali oss
        """
        self.connect()

        # get image path
        if not image_path_local:
            image_path_local = self.save_clipboard_data(self.image_name)

        image_path_oss = self.parser_path_in_oss(self.image_name)

        # upload to oss
        ret = self.bucket.put_object_from_file(
            image_path_oss, image_path_local)

        url = ret.resp.response.url
        results = self.parser_results(url)
        return results


if __name__ == '__main__':
    # test
    import sys
    from settings_self import OSS_INFO
    # OSS_INFO['image_name'] = sys.argv[1]
    uploader = Uploader(**OSS_INFO)
    uploader.upload()
