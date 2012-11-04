#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

import json,urllib2

PERMS={
    1:None,#" 	Пользователь разрешил отправлять ему уведомления.",
    2:'friends',# " 	Доступ к друзьям.",
    4:None,#' 	Доступ к фотографиям.',
    8:None,#' 	Доступ к аудиозаписям.',
    16:None,#' 	Доступ к видеозаписям.',
    32:None,#' 	Доступ к предложениям.',
    64:None,#' 	Доступ к вопросам.',
    128:None,#' 	Доступ к wiki-страницам.',
    256:None,#' 	Добавление ссылки на приложение в меню слева.',
    512:None,#' 	Добавление ссылки на приложение для быстрой публикации на стенах пользователей.',
    1024:None,#' 	Доступ к статусам пользователя.',
    2048:None,#' 	Доступ заметкам пользователя.',
    4096:None,#' 	(для Desktop-приложений) Доступ к расширенным методам работы с сообщениями.',
    8192:None,#' 	Доступ к обычным и расширенным методам работы со стеной.Внимание, данное право доступа недоступно для сайтов (игнорируется при попытке авторизации).',
    32768:None,#' 	Доступ к функциям для работы с рекламным кабинетом.',
    131072:None,#' 	Доступ к документам пользователя.',
    262144:None,#' 	Доступ к группам пользователя.',
    524288:None,#' 	Доступ к оповещениям об ответах пользователю.',
    1048576:None,#' 	Доступ к статистике групп и приложений пользователя, администратором которых он является. '}
    }
from vk_friends import friends


class VK(object):
    """
    base class for VK API
    """

    def __init__(self,app,uid,token):
        self.__app=app
        self.__token=token
        self.__uid=uid
        self.__error={}
        self.__result={}

        if self.handler('getUserSettings',uid=self.__uid):
            self.__perms = int(self.__result)
            for permission in PERMS.keys():
                if self.__perms&permission==permission and PERMS[permission]:
                    setattr(self,PERMS[permission],eval(PERMS[permission]+"(self.handler)"))
    def get_uid(self):
        return self.__uid
    def get_appid(self):
        return self.__app
    def get_error(self):
        return self.__error
    def get_result(self):
        return self.__result
    def get_perms(self):
        return self.__perms


    def handler(self,method,**kwargs):
        """
        get response
        """
        url = self.__makeUrl(method,**kwargs)
        res=json.loads(urllib2.urlopen(url).read())
        if res.has_key("error"):
            self.__error=res
            return False
        self.__result=res["response"]
        return True



    def __makeUrl(self,method,**kwargs):
        """
        generate request uri
        """
        url="https://api.vk.com/method/{0}?{1}access_token={2}"
        data=""
        for item in kwargs.items():
            if type(item[1]) in [list,tuple]:
                data+="{0}={1}&".format( item[0],",".join([str(i) for i in item[1]]) )
            else:
                data+="{0}={1}&".format( item[0],item[1])
        return url.format(method,data,self.__token)

    @staticmethod
    def GetPopupUrl(app_id=None,scope = [
                                        "notify",# 	Пользователь разрешил отправлять ему уведомления.
                                        "friends",# 	Доступ к друзьям.
                                        "photos",# 	Доступ к фотографиям.
                                        "audio",# 	Доступ к аудиозаписям.
                                        "video",# 	Доступ к видеозаписям.
                                        "docs",# 	Доступ к документам.
                                        "notes",# 	Доступ заметкам пользователя.
                                        "pages",# 	Доступ к wiki-страницам.
                                        "offers",# 	Доступ к предложениям (устаревшие методы).
                                        "questions",# 	Доступ к вопросам (устаревшие методы).
                                        "wall",# 	Доступ к обычным и расширенным методам работы со стеной.
                                        "groups",# 	Доступ к группам пользователя.
                                        "messages",# 	(для Standalone-приложений) Доступ к расширенным методам работы с сообщениями.
                                        "notifications",# 	Доступ к оповещениям об ответах пользователю.
                                        "stats",# 	Доступ к статистике групп и приложений пользователя, администратором которых он является.
                                        "ads",# 	Доступ к расширенным методам работы с рекламным API.
                                        "offline"# 	Доступ к API в любое время со стороннего сервера.
                                    ]):
        """
        http://vk.com/pages?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
        """
        if not app_id:
            raise ValueError,"API ID is not defined."
        if not scope or type(scope) not in [tuple,list]:
            raise ValueError,"Scope must be list or tuple type"

        url="http://oauth.vk.com/authorize?client_id={0}&scope={1}&redirect_uri=http://oauth.vk.com/blank.html&display=popup&response_type=token"
        return url.format(app_id,",".join(scope))




