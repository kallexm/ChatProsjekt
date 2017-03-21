# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from Chat import Chat

class Client:
    """
    This is the chat client class
    """
    chat = Chat()

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        # TODO: Finish init process with necessary code
        self.run()
        msgRecv = MessageReceiver(self, self.connection)
        

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.chat.run()


    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        chat.DisplayMsgToUser(message)
        

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
        
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)