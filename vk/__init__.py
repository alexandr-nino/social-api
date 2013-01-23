'''
doc string
'''
#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'
import json
import urllib2

PERMS = {
    1: None,  # Notification
    2: 'friends',  # Friends
    4: None,  # Photos
    8: None,  # Music
    16: 'video',  # Videos
    32: None,  # Apps
    64: None,  # asks
    128: None,  # Wiki pages
    256: None,  # Left menu app link
    512: None,  # Link for fast comment link to app on walls
    1024: None,  # Statuses
    2048: None,  # Notes
    4096: None,  # more methods for messages
    # Desktop only
    8192: None,  # Wall. not for sites
    32768: None,  # ADS
    131072: 'docs',  # docs
    262144: None,  # Groups
    524288: None,  # notify answers
    1048576: None,  # Stats Groups and Apps if i'm admin
}
AVAILIABLE_PERMS = filter(lambda x: x, PERMS.itervalues())


from vk_friends import friends
from vk_video import video
from vk_documents import docs


class VK(object):
    """
    base class for VK API
    """
    def __init__(self, app, uid, token):
        """

        """
        self.__app = app
        self.__token = token
        self.__uid = uid
        self.__error = {}
        self.__result = {}

        if self.handler('getUserSettings', uid=self.__uid):
            self.__perms = int(self.__result)
            for permission in PERMS.keys():
                if (self.__perms & permission == permission)\
                        and PERMS[permission]:
                    setattr(self,
                            PERMS[permission],
                            eval(PERMS[permission] + "(self.handler)"))

    def get_uid(self):
        """
        return current user id
                """
        return self.__uid

    def get_app_id(self):
        """
                return current appication id
                """
        return self.__app

    def get_error(self):
        """
                return last error
                """
        return self.__error

    def get_result(self):
        """
                return result
                """
        return self.__result

    def get_perms(self):
        """
                return app permissions for current user
                """
        return self.__perms

    def handler(self, method, **kwargs):
        """
        global request handler
        """
        url = self._make_url(method, **kwargs)
        response = json.loads(urllib2.urlopen(url).read())
        if "error" in response:
            self.__error = response
            return False
        self.__result = response["response"]
        return True

    def _make_url(self, method, **kwargs):
        """
        generate request uri
        """
        url = "https://api.vk.com/method/{0}?{1}access_token={2}"
        data = ""
        for item in kwargs.items():
            if type(item[1]) in [list, tuple]:
                data += "{0}={1}&".format(
                        item[0],
                        ",".join([str(i) for i in item[1]]))
            else:
                data += "{0}={1}&".format(item[0], item[1])
        return url.format(method, data, self.__token)

    @staticmethod
    def get_popup_url(app_id, scope=AVAILIABLE_PERMS):
        """
        http://vk.com/pages?oid=-1&p=Права_доступа_приложенийu
        """
        assert type(app_id) == int
        assert type(scope) in [list, tuple]

        url = "http://oauth.vk.com/authorize?" \
              "client_id={0}&" \
              "scope={1}&" \
              "redirect_uri=http://oauth.vk.com/blank.html&" \
              "display=popup&" \
              "response_type=token"
        return url.format(app_id, ",".join(scope))
