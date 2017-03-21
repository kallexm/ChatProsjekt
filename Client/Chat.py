# -*- coding: utf-8 -*-
from threading import Thread

class Chat(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        loggedIn = False
        print("Starting chat")
        while True:
            data = self.getInputFromUser()
            if data[0:len("login")] == "login":
                print("logged in as:", end='')
                print(data[len("login"):])
                self.login(data[len("login")+1:])
            elif data[0:len("logout")] == "logout":
                print("logged out")
            else:
                print(data)

    def DisplayMsgToUser(self, message):
        print(message)

    def getInputFromUser(self):
        inputData = input("->")
        return inputData

    def login(self, username):
        data = {'request': 'login',
                'content': username
               }
        Client.send_payload(data)

    def logout(self):
        data = {'request': 'logout',
                'content': None
               }
        Client.send_payload(data)

    def sendMsg(self, msg):
        data = {'request': 'msg',
                'content': msg
               }
        Client.send_payload(data)

    def getHelp(self):
        data = {'request': 'help',
                'content': None
               }
        Client.send_payload(data)

    def getNameList(self):
        data = {'request': 'names',
                'content': None
               }
        Client.send_payload(data)
