import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print("No match in possible responses")

    def parse_error(self, payload):
        return payload


    def parse_info(self, payload):
        return payload

    def parse_message(self, payload):
        return payload

    def parse_history(self, payload):
        return payload
        