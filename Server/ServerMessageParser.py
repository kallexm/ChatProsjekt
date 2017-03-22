# -*- coding: utf-8 -*-

import json

class ServerMessageParser():
    def __init__(self):
                
        self.possible_responses = {
        'login': self.parse_login,
        'logout': self.parse_logout,
        'msg': self.parse_msg,
        'names': self.parse_names,
        'help': self.parse_help
        }

    def parse(self, payload):
        # Change some of this implementation
        payload = json.loads(payload) # decode the JSON object
        if payload['request'] in self.possible_responses:
            return self.possible_responses[payload['request']](payload)
        else:
            print("Response not valid")
            # Response not valid

                                     
    def parse_login(self, payload):
        return payload
                                        
    def parse_logout(self, payload):
        return payload
                                        
    def parse_msg(self, payload):
        return payload
                                        
    def parse_names(self, payload):
        return payload
        
    def parse_help(self, payload):
        return payload
