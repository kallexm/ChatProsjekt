# -*- coding: utf-8 -*-
import socketserver
import socket
import time
import json
import errno
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
                    self.handleSendMsgRequest(parsedMsg['content'], name, isLoggedIn)
            
                elif parsedMsg['request'] == 'names':
                    self.handleNamelistRequest(name, isLoggedIn)
            
                elif parsedMsg['request'] == 'help':
                    self.handleHelpRequest()
         


    def handleLoginRequest(self, msgContent, name, isLoggedIn):
        if not str.isalnum(msgContent):
            data = createResponseStruct("", 'error', 'Error: Username can only contain alphanumericals')
        elif msgContent in connections_logged_in.keys():
            data = createResponseStruct("", 'error', 'Error: Username already in use')
        elif isLoggedIn:
            data = createResponseStruct("", 'error', 'Error: Already loged in as: ' + name)
        else:
            connections_logged_in[msgContent] = self.connection
            #data = createResponseStruct("", 'info', 'login as: ' + msgContent + ' successful')
            isLoggedIn = True
            name = msgContent
            sendHistoryListMessage(name)
            return name, isLoggedIn

        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
        
        return name, isLoggedIn
    



    def handleLogoutRequest(self, name, isLoggedIn):
        if not isLoggedIn:
            data = createResponseStruct("", 'error', 'Error must be logged inn')
        else:
            del connections_logged_in[name]
            data = createResponseStruct("", 'info', 'Log out successful')
            isLoggedIn = False
            name = ""
        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
        return name, isLoggedIn




    def handleHelpRequest(self):
        helpMessage = "\n========================[help]========================\nlogin [username]\n - Use command to log on to the chat server\n\nlogout\n - Use command to logout\n\nhelp\n - Use command to show this message\n\nlist\n - Use command to show names of all the logged on users\n\nIf you are logged in you can write messages by\ntyping you message followed by ENTER.\n========================[help]========================\n"
        data = createResponseStruct("", 'info', helpMessage)
        sendMsg = json.dumps(data)
        rawSendMsg = sendMsg.encode()
        self.connection.send(rawSendMsg)
    



    def handleNamelistRequest(self, name, isLoggedIn):
        if isLoggedIn:
            userList = "\n=======================[users]========================\n"
            for user in connections_logged_in:
                userList = userList+user+"\n"
            userList = userList+"=======================[users]========================\n\n"
            data = createResponseStruct("", 'info', userList)
            sendMsg = json.dumps(data)
            rawSendMsg = sendMsg.encode()
            self.connection.send(rawSendMsg)
        else:
            data = createResponseStruct("", 'error', 'Error: must be logged in to request list of users')
            sendMsg = json.dumps(data)
            rawSendMsg = sendMsg.encode()
            self.connection.send(rawSendMsg)
    



    def handleSendMsgRequest(self, msgContent, name, isLoggedIn):
        if isLoggedIn:
            data = createResponseStruct(name, 'message', msgContent)
            conversation_history.append(data)

            brokenConn = {}
            for user in connections_logged_in:
                sendMsg = json.dumps(data)
                rawSendMsg = sendMsg.encode()
                try:
                    connections_logged_in[user].send(rawSendMsg)
                except socket.error as e:
                    print("Error: connection broke to "+user+", closing connection")
                    brokenConn[user] = connections_logged_in[user]
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        print("EPIPE error")
                    else:
                        print("unknown error")
            for user in brokenConn:
                del connections_logged_in[user]

        else:
            data = createResponseStruct("", 'error', 'Error: must be logged in to send message')
            sendMsg = json.dumps(data)
            rawSendMsg = sendMsg.encode()
            self.connection.send(rawSendMsg)
    



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True




def createResponseStruct(sender, response, content):
    curentTime = time.strftime("%X")
    if response == 'error' or response == 'info' or response == 'history':
        sender = 'Server'
    return {'timestamp': curentTime,'sender': sender, 'response': response, 'content': content}




def sendHistoryListMessage(to):
    data = createResponseStruct("", "history", conversation_history)
    sendMsg = json.dumps(data)
    rawSendMsg = sendMsg.encode()
    connections_logged_in[to].send(rawSendMsg)




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

