#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

from urllib import urlencode
from urllib2 import urlopen
import httplib as http
import json


class yandex:
    def __init__(self,app_id,app_code,sandbox=True):
        self.is_sandbox=sandbox
        self.id=app_id
        self.code=app_code
        self.token=False
    def getBase(self):
        coon=False
        if self.is_sandbox:
            conn=http.HTTPSConnection("api-sandbox.direct.yandex.ru")
        else:
            conn=http.HTTPSConnection("soap.direct.yandex.ru")
        data = {
            "locale": "ru",
            "login":self.login,
            "application_id":self.id,
            "token":self.token
        }
        headers={"Content-Type":"application/json; charset=utf-8"}
        return data,conn,headers
    def send(self,conn,data,head):
        conn.request("POST","/json-api/v4/",json.dumps(data,encoding="u8"),head)
        req = conn.getresponse()
        data = json.loads(req.read(),encoding="u8")
        conn.close()
        return data
    def getTokenByUser(self,login,passw):
        data =dict(
                    grant_type="password",
                    username=login,
                    password=passw,
                    client_id=self.id,
                    client_secret=self.code
                    )
        data = urlencode(data)
        headers={
            "Content-type":"application/x-www-form-urlencoded"
        }
        conn=http.HTTPSConnection("oauth.yandex.ru")
        conn.request("POST","/token",data,headers)
        req = conn.getresponse()
        data=json.loads(req.read())
        conn.close()

        if "error_code" in data:
            return False,data
        else:
            self.login=login
            self.token=data["access_token"]
            return True
    def GetClientsList(self):
        data,conn,head=self.getBase()
        data["method"]="GetClientsList"
        data=self.send(conn,data,head)
        res=[]
        if "data" in data:
            for i in data["data"]:
                res+=[{"Login":i["Login"],"FIO":i["FIO"]}]
            return True,res
        else:return False,data

    def GetCampaignsListFilter(self,**params):
        data,conn,head = self.getBase()

        data["method"]="GetCampaignsListFilter"
        data["param"]={}
        for k,v in params.items():
            data["param"][k]=v


        data=self.send(conn,data,head)
        if "data" in data:
            return True,[i["CampaignID"] for i in data["data"]]
        else:
            return False,data
    def GetCampaignsParams(self,**params):
        data,conn,head=self.getBase()
        data["method"]="GetCampaignsParams"
        data["param"]={ #"CampaignIDS":cmp_list
                         }
        for k,v in params.items():
            data["param"][k]=v

        data=self.send(conn,data,head)
        if "data" in data:
            return True,data["data"]
        else:return False,data
    def GetSummaryStat(self,**params):
        data,conn,head = self.getBase()
        data["method"]="GetSummaryStat"
        data["param"]={}

        for k,v in params.items():
            data["param"][k]=v
        data = self.send(conn,data,head)
        if "data" in data:
            return True,data
        else:
            return False,data