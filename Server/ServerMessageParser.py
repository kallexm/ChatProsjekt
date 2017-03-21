# -*- coding: utf-8 -*-


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
        print("Parse")
        # Change some of this implementation
        payload = json.loads(payload) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("Response not valid")
            # Response not valid

                                     
    def parse_login(self, payload):
        print("parse_login")
        return payload
                                        
    def parse_logout(self, payload):
        print("parse_logout")
        return payload
                                        
    def parse_msg(self, payload):
        print("parse_msg")
        return payload
                                        
    def parse_names(self, payload):
        print("parse_names")
        return payload
		
    def parse_help(self, payload):
        print("parse_help")
        return payload
