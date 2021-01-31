from flask import Flask, request, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse
from nlphandler import respond
from status import statusChange, getUserStatuses
import os
from threading import Thread
import json
import os
from dotenv import load_dotenv
from slack_util import SlackClientHandler
from datetime import datetime, timedelta
from threading import Timer

# comment out when debug mode
os.environ.pop("FLASK_APP")
os.environ.pop("FLASK_ENV")

load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

slackClientHandler = SlackClientHandler(SLACK_TOKEN)
    
def get_next_time():
    x=datetime.today()
    y = x.replace(day=x.day, hour=21, minute=37, second=0, microsecond=0)
    
    if y < x:
        y += timedelta(days=1)
    delta_t=y-x

    secs=delta_t.total_seconds()
    return(secs)

def send_morning_message():
    slackClientHandler.send_message("Hello, do you have any tasks today that I don't know about?")
    t = Timer(get_next_time(), send_morning_message)
    t.start()

t = Timer(get_next_time(), send_morning_message)
t.start()

app = Flask(__name__)
        

@app.route('/slack', methods=['POST'])
def slack_event_hook():
    json_dict = request.get_json()
    app.logger.info(json_dict)

    try:

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
                slackClientHandler.send_message(statusChange(json_dict["event"]["user"]["profile"]["status_text"],json_dict["event"]["user"]["profile"]["real_name_normalized"]))
                return {"status": 201}
                #event user profile status_text


        elif "event" in json_dict and "type" in json_dict["event"]:
            if json_dict["event"]["type"] == "message" and 'bot_id' not in json_dict['event']:
                slackClientHandler.send_message(respond(json_dict["event"]["text"], slackClientHandler.get_user_id(json_dict["event"]["user"])), json_dict["event"]["channel"])
                return {"status": 201}
            elif json_dict["event"]["type"] == "user_change":
                slackClientHandler.send_message(statusChange(json_dict["event"]["user"]["profile"]["status_text"],json_dict["event"]["user"]["profile"]["real_name_normalized"]))
                slackClientHandler.send_message(getUserStatuses())
                return {"status": 201}
                #event user profile status_text
    except:
        return {"status": 500}

@app.route('/discord', methods=['POST'])
def discord_event_hook():
    json_dict = request.get_json()
    response = respond(json_dict["text"], json_dict["user"])
    return {"status": 201, "response": response}

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()
