# -*- coding:u8 -*-
__author__ = 'alexandr'


class video(object):
    def __init__(self,callback):
        self.clb = callback

    def search(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=video.search
                """
        return self.clb('video.search', **kwargs)

    def get(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=video.get
                """
        return self.clb('video.get', **kwargs)
