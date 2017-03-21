# -*- coding: utf-8 -*-
from threading import Thread
from Client import Client

class Chat(Thread):

    def __init__(self):
		
	
    def run(self):
	
    def DisplayMsgToUser(self, message):
		print(message)
	
    def getInputFromUser(self):
		inputData = input(":")
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
	