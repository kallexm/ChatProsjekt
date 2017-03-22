# -*- coding: utf-8 -*-
import socketserver
import time
import json
from ServerMessageParser import ServerMessageParser 

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connections_logged_in = {}
conversation_history = []


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """ 
    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        isLoggedIn = False
        name = ""    
        # Loop that listens for messages from the client

        parser = ServerMessageParser()
        print("Connection established")
        while True:
            
            received_string = self.connection.recv(4096)
            
            # TODO: Add handling of received payload from client
            if received_string:
                msgFromClient = received_string.decode()
                parsedMsg = parser.parse(msgFromClient)
            
                if parsedMsg['request'] == 'login':
                    name, isLoggedIn = self.handleLoginRequest(parsedMsg['content'], name, isLoggedIn)
                elif parsedMsg['request'] == 'logout':
                    name, isLoggedIn = self.handleLogoutRequest(name, isLoggedIn)
            
                elif parsedMsg['request'] == 'msg':
                    self.handleSendMsgRequest(parsedMsg['content'])
            
                elif parsedMsg['request'] == 'names':
                    self.handleNamelistRequest()
            
                elif parsedMsg['request'] == 'help':
                    self.handleHelpRequest()
            
    def handleLoginRequest(self, msgContent, name, isLoggedIn):
        if not str.isalnum(msgContent):
            print("not isalnum")
            data = createresponseStruct("", 'error', 'Error: Username can only contain alphanumericals')
        elif msgContent in connections_logged_in.keys():
            data = createresponseStruct("", 'error', 'Error: Usernam alrady in use')
            print("Username alrady in use")
        elif isLoggedIn:
            data = createresponseStruct("", 'error', 'Error: Allrady loged in as: ' + name)
            print("Username alrady logged in")
        else:
            connections_logged_in[msgContent] = self
            data = createresponseStruct("", 'info', 'login as: ' + msgContent + ' successful')
            isLoggedIn = True
            name = msgContent
        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
        return name, isLoggedIn
    
    def handleLogoutRequest(self, name, isLoggedIn):
        if not isLoggedIn:
            data = createresponseStruct("", 'error', 'Error must be logged inn')
        else:
            del connections_logged_in[name]
            data = createresponseStruct("", 'info', 'Log out successful')
            isLoggedIn = False
            name = ""
        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
        return name, isLoggedIn

    def handleHelpRequest(self):
        pass
    
    def handleNamelistRequest(self):
        pass
    
    def handleSendMsgRequest(self, msgContent):
        pass
    

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True



def createresponseStruct(sender, response, content):
    curentTime = time.strftime("%X")
    if response == 'error' or response == 'info' or response == 'history':
        sender = 'Server'
    return {'timestamp': curentTime,'sender': sender, 'response': response, 'content': content}


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
