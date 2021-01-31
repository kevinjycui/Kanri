from flask import Flask, request, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse
from nlphandler import respond
import os
from threading import Thread
import json
import os
from dotenv import load_dotenv
from slack_util import SlackClientHandler


load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

slackClientHandler = SlackClientHandler(SLACK_TOKEN)

def sendStatusChangeMessage(newStatus, userName):
    response = ''

    if newStatus == "In a meeting":
        response = userName + " is now in a meeting."
    else:
        response = userName + " is now " + newStatus
    return response
    

app = Flask(__name__)
        

@app.route('/slack', methods=['POST'])
def event_hook():
    json_dict = request.get_json()
    app.logger.info(json_dict)

    if json_dict["token"] != SLACK_VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict and json_dict["type"] == "url_verification":
        response_dict = {"challenge": json_dict["challenge"]}
        return response_dict

    elif "event" in json_dict and "type" in json_dict["event"]:
        if json_dict["event"]["type"] == "message" and 'bot_id' not in json_dict['event']:
            slackClientHandler.send_message(respond(json_dict["event"]["text"], slackClientHandler.get_user_id(json_dict["event"]["user"])), json_dict["event"]["channel"])
            return {"status": 201}
        elif json_dict["event"]["type"] == "user_change":
            slackClientHandler.send_message(sendStatusChangeMessage(json_dict["event"]["user"]["profile"]["status_text"],json_dict["event"]["user"]["profile"]["real_name_normalized"]))
            #slackClientHandler.send_message("test")
            return {"status": 201}
            #event user profile status_text

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

