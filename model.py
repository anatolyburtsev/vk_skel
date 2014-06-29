# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal
from threading import Thread
import json
import urllib.request
from settings import *

class Model(QObject):
    friendsReady = pyqtSignal(str)
    try:
        accessFile = open(confFile, 'r')
    except IOError:
        accessToken = ""
    else:
        accessToken = accessFile.read()
        accessFile.close()

    def setAccessToken(self, accessToken):
        self.accessToken = accessToken
        accessFile = open(confFile, 'w')
        accessFile.write(accessToken)	
        accessFile.close()

    # Запускает getFriends в отдельном потоке. Если все делать в одном потоке, интерфейс будет висеть
    # Для запуска одного метода вряд ли будет заметно, но если делать что-то тяжелое, то еще как будет
    def getFriendsAsync(self):
        thread = Thread(target = self.getFriends)
        thread.setDaemon(True)
        thread.start()

    def getFriends(self):
        with urllib.request.urlopen(getFriendsUrl.format(accessToken = self.accessToken)) as url:
            res = url.read()
        resDict = json.loads(res.decode('utf-8'))
        friendsStr = u"\n".join([u"{lastName} {firstName}".format(
                     lastName = friend["last_name"], firstName = friend["first_name"])
                     for friend in resDict["response"]])
        self.friendsReady.emit(friendsStr)
