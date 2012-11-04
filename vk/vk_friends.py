# -*- coding: u8 -*-
__author__ = '_killed_'


class friends(object):
    def __init__(self,vk_get):
        self.vk_get = vk_get # VK.get(...)

    def get(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=friends.get
        """
        return self.vk_get('friends.get',**kwargs)

    def getAppUsers(self):
        """
        http://vk.com/pages?oid=-1&p=friends.getAppUsers
        """
        return self.vk_get('friends.getAppUsers')

    def getOnline(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=friends.getOnline
        """
        return self.vk_get('friends.getOnline', **kwargs)

    def getMutual(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=friends.getMutual
        """
        return self.vk_get('friends.getMutual', **kwargs)

    def areFriends(self, **kwargs):
        """
        http://vk.com/pages?oid=-1&p=friends.areFriends
        """
        return self.vk_get('friends.areFriends', **kwargs)