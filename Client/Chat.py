# -*- coding: utf-8 -*-
from threading import Thread
#from Client import Client

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
                print("logged out")
                self.logout()
            elif data[0:len("help")] == "help":
            	print("help: ")
            	self.getHelp()
            elif data[0:len("List names")] == "List names":
            	print("Name: ")
            	self.getNameList()
            else:
                print(data)
                self.sendMsg(data)

    def DisplayMsgToUser(self, message):
        print(message)

    def getInputFromUser(self):
        inputData = input("->")
        return inputData

    def login(self, username):
        data = {'request': 'login',
                'content': username
               }
        self.client.send_payload(data)

    def logout(self):
        data = {'request': 'logout',
                'content': None
               }
        self.client.send_payload(data)

    def sendMsg(self, msg):
        data = {'request': 'msg',
                'content': msg
               }
        self.client.send_payload(data)

    def getHelp(self):
        data = {'request': 'help',
                'content': None
               }
        self.client.send_payload(data)

    def getNameList(self):
        data = {'request': 'names',
                'content': None
               }
        self.client.send_payload(data)
