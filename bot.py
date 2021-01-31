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
# os.environ.pop("FLASK_APP")
# os.environ.pop("FLASK_ENV")

load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

slackClientHandler = SlackClientHandler(SLACK_TOKEN)

notify_hour = 8
notify_minute = 0
notify_second = 0



def get_next_time():
    global notify_hour, notify_minute, notify_second
    
    x=datetime.today()
    y = x.replace(day=x.day, hour=notify_hour, minute=notify_minute, second=notify_second, microsecond=0)
    
    if y < x:
        y += timedelta(days=1)
    delta_t=y-x

    secs=delta_t.total_seconds()
    return(secs)

def send_morning_message():
    slackClientHandler.send_message("Hello everyone! Tell me about your tasks for today in the DMs.")
    t = Timer(get_next_time(), send_morning_message)
    t.start()

t = Timer(get_next_time(), send_morning_message)
t.start()

def set_new_time(h, m, s):
    global t, notify_hour, notify_minute, notify_second

    notify_hour = h
    notify_minute = m
    notify_second = s
    t.cancel()
    t = Timer(get_next_time(), send_morning_message)
    t.start()

app = Flask(__name__)
        

@app.route('/slack', methods=['POST'])
def slack_event_hook():
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
            send_morning_message()
            slackClientHandler.send_message(statusChange(json_dict["event"]["user"]["profile"]["status_text"],json_dict["event"]["user"]["profile"]["real_name_normalized"]), "C01LBJ5NDM3")
            return {"status": 201}
            #event user profile status_text

    return {"status": 500}

@app.route('/morning', methods=['POST'])
def morning_event_hook():
    try:
        params = list(map(int, request.values.get('text', '').split(' ')))
        assert len(params) <= 3
        while len(params) < 3:
            params.append(0)

        set_new_time(params[0], params[1], params[2])
        assert params[0] >= 0 and params[0] < 24
        assert params[1] >= 0 and params[1] < 60
        assert params[2] >= 0 and params[2] < 60
        return 'New morning time set to %d:%d:%d. You will receive a standup announcement at this time.' % tuple(params)
    except Exception as e:
        print(e)
        return 'Failed to set new time, please use format /morning h m s'
    return {"status": 201}

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()
