#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

from PyQt4 import QtWebKit,QtGui,QtCore


class vk_OAuth(QtGui.QDialog):
    def __init__(self,auth_page=None,parent=None):
        super(C_OAuthWindow,self).__init__(parent)
        self.resize(640,480)

        self.web_view = QtWebKit.QWebView(self)
        self.web_view.load(QtCore.QUrl(auth_page))
        self.connect(self.web_view,QtCore.SIGNAL("loadFinished(bool)"),self.redirectEvent)
    def run(self):
        if self.exec_():
            return True,self.result
        else:
            return False,self.result

    def redirectEvent(self,hz=None):
        page = str(self.web_view.url().toString())
        if "blank.html#" in page:
            uri=page.split("#")[-1]
            uri=uri.split("&")
            uri=[i.split("=") for i in uri]
            self.result=dict(uri)
            if "error" in self.result:
                self.reject()
            else:
                self.accept()

    def resizeEvent(self, QResizeEvent):
        self.web_view.resize(QResizeEvent.size())