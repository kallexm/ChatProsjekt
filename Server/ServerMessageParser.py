# -*- coding: utf-8 -*-


class ServerMessageParser():
	def __init__(self):
		
		self.possible_responses = {
            'login': self.parse_login,
            'logout': self.parse_logout,
			'msg': self.parse_msg,
			'names': self.parse_names,
			'help': self.parse_help,
        }

	def parse(self, payload):
	
	
	
	def parse_login(self, payload):
	
	
	def parse_logout(self, payload):
	
	
	def parse_msg(self, payload):
	
	
	def parse_names(self, payload):
	
	
	def parse_help(self, payload):

	