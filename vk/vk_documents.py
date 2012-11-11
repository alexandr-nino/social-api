# -*- coding:u8 -*-
__author__ = 'alexandr'

class docs(object):
    def __init__(self,callback):
        self.clb = callback

    def get(self, **kwargs):
        """
                http://vk.com/pages?oid=-1&p=docs.get
                """
        return self.clb('docs.get', **kwargs)

    def getById(self, **kwargs):
        """
            http://vk.com/pages?oid=-1&p=docs.getById
                """
        return self.clb('docs.getById',**kwargs)