# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection

        # TODO: Finish initialization of MessageReceiver
        

    def run(self):
        parser = MessageParser()
        # TODO: Make MessageReceiver receive and handle payloads
        print("Start messageReceiver")
        while True:
            rawRecvMessage = self.connection.recv(4096)
            if rawRecvMessage:
                recvMessage = rawRecvMessage.decode()
                payload = parser.parse(recvMessage)

                if payload['response'] == 'error':
                    self.errorHandler(payload)
                elif payload['response'] == 'info':
                    self.infoHandler(payload)
                elif payload['response'] == 'history':
                    self.historyHandler(payload)
                elif payload['response'] == 'message':
                    self.messageHandler(payload) 



    def errorHandler(self, payload):
        self.client.receive_message(payload['content'])

    def infoHandler(self, payload):
        self.client.receive_message(payload['content'])

    def historyHandler(self, payload):
        msgStr = "Login Successful\nHistory log:\n"
        for message in payload['content']:
            msgStr = msgStr+message['sender']+" ["+message['timestamp']+"]: "+message['content']+"\n"
        self.client.receive_message(msgStr)

    def messageHandler(self, payload):
        msgStr = payload['sender']+" ["+payload['timestamp']+"]: "+payload['content']
        self.client.receive_message(msgStr)