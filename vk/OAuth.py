#!/usr/bin/python
# -*- coding:u8 -*-
'''
doc string
'''
__author__ = '_killed_'

from PyQt4 import QtWebKit, QtGui, QtCore


class vk_OAuth(QtGui.QDialog):
    """
    get access_token from vk.com
    """
    def __init__(self, auth_page = None, parent = None):
        """
        init QDialog with QWebView
        """
        super(vk_OAuth, self).__init__(parent)
        self.resize(640, 480)

        self.web_view = QtWebKit.QWebView(self)
        self.web_view.load(QtCore.QUrl(auth_page))
        self.connect(self.web_view,
                        QtCore.SIGNAL("loadFinished(bool)"),
                        self.redirectEvent)

    def run(self):
        """
        auth runner
        """
        if self.exec_():
            return True, self.result
        else:
            return False, self.result

    def redirectEvent(self, QEvent=None):
        """
        check redirect page for get response from URI
        """
        page = str(self.web_view.url().toString())
        if "blank.html#" in page:
            uri = page.split("#")[-1]
            uri = uri.split("&")
            uri = [i.split("=") for i in uri]
            self.result = dict(uri)
            if "error" in self.result:
                self.reject()
            else:
                self.accept()

    def resizeEvent(self, QResizeEvent):
        """
               resize QWebView with Dialog window
                """
        self.web_view.resize(QResizeEvent.size())