#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

import json,urllib2

class VK(object):
    def __init__(self,app,uid,token):
        self.app=app
        self.token=token
        self.uid=uid
        self.error={}
        self.result={}


    def get(self,method,**kwargs):
        url = self.makeUrl(method,**kwargs)
        res=json.loads(urllib2.urlopen(url).read())
        if res.has_key("error"):
            self.error=res
            return False
        self.result=res["response"]
        return True



    def makeUrl(self,method,**kwargs):
        url="https://api.vk.com/method/{0}?{1}access_token={2}"
        data=""
        for item in kwargs.items():
            if type(item[1]) in [list,tuple]:
                data+="{0}={1}&".format( item[0],",".join([str(i) for i in item[1]]) )
            else:
                data+="{0}={1}&".format( item[0],item[1])
        return url.format(method,data,self.token)





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
        if not app_id:
            raise ValueError,"API ID is not defined."
        if not scope or type(scope) not in [tuple,list]:
            raise ValueError,"Scope must be list or tuple type"

        url="http://oauth.vk.com/authorize?client_id={0}&scope={1}&redirect_uri=http://oauth.vk.com/blank.html&display=popup&response_type=token"
        return url.format(app_id,",".join(scope))


    @staticmethod
    def GetToken(email,passw,app_id):

        data={"email":email,"pass":passw}
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPSConnection("vk.com")
        conn.request("POST","/login.php",urllib.urlencode(data),headers)
        resp = conn.getresponse()
        conn.close()
        head = resp.getheader("Set-Cookie")
        remixsid=re.findall(r'remixsid=([^;]+)',head)[0]
        headers={"Cookie":"remixsid="+remixsid+";"}
        cookie=headers

        #url = "http://oauth.vk.com/authorize?client_id={0}&scope=notify,friends,photos,audio,video,docs,notes,pages,offers,questions,wall,groups,messages,notifications,stats,ads,offline&redirect_uri=http://oauth.vk.com/blank.html&display=popup&response_type=token"
        data={"client_id":app_id,
              "scope":"notify,friends,photos,audio,video,docs,notes,pages,offers,questions,wall,groups,messages,notifications,stats,ads,offline",
              "redirect_uri":"http://oauth.vk.com/blank.html",
              "display":"popup",
              "response_type":"token"
        }

        headers.update(cookie)

        conn=httplib.HTTPSConnection("oauth.vk.com")
        conn.request("GET",url="/authorize?"+urllib.unquote_plus(urllib.urlencode(data)),body=None,headers=headers)
        r = conn.getresponse()
        page=r.read().decode("cp1251")


        url=re.findall(r'location.href = "([^"]+)',page)[0]

        conn.request("GET","/"+url.split("/")[-1],body=None,headers=headers)
        r=conn.getresponse()
        conn.close()
        uri=r.getheader("location").split("#")[-1]
        data = uri.split("&")
        data=dict([i.split("=") for i in data])
        return data["access_token"],data["user_id"]





