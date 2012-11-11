# -*- coding:u8 -*-
__author__ = 'alexandr'


class video(object):
    def __init__(self,callback):
        self.clb = callback
    def search(self,**kwargs):
        return self.clb('video.search',**kwargs)
    def get(self,**kwargs):
        return self.clb('video.get',**kwargs)