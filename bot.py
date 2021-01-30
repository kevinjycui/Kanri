from flask import Flask, request, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse
from processor import respond
import os
from threading import Thread
import json
import os
from dotenv import load_dotenv
from slack-util import SlackClientHandler

load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

slackClientHander = SlackClientHandler()

app = Flask(__name__)
        

@app.route('/slack', methods=['POST'])
def event_hook():
    json_dict = request.get_json()
    app.logger.info(json_dict)

    if json_dict["token"] != SLACK_VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict


    return {"status": 500}

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()

