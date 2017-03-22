# -*- coding: utf-8 -*-
from threading import Thread

class Chat(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.daemon = True
        self.client = client

    def run(self):
        loggedIn = False
        print("Starting chat")
        while True:
            data = self.getInputFromUser()
            if data[0:len("login")] == "login":
                self.login(data[len("login")+1:])
            elif data[0:len("logout")] == "logout":
                self.logout()
            elif data[0:len("help")] == "help":
            	self.getHelp()
            elif data[0:len("list")] == "list":
            	self.getNameList()
            else:
                self.sendMsg(data)

    def DisplayMsgToUser(self, message):
        print(message)

    def getInputFromUser(self):
        inputData = input()
        return inputData

    def login(self, username):
        data = createRequest('login', username)
        self.client.send_payload(data)

    def logout(self):
        data = createRequest('logout', None)
        self.client.send_payload(data)

    def sendMsg(self, msg):
        data = createRequest('msg', msg)
        self.client.send_payload(data)

    def getHelp(self):
        data = createRequest('help', None)
        self.client.send_payload(data)

    def getNameList(self):
        data = createRequest('names', None)
        self.client.send_payload(data)


def createRequest(request, content):
    return {'request': request, 'content': content}