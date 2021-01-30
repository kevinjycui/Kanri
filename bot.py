from flask import Flask, request, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse
from processor import respond
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread
import sys

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter("20f2f470e8cee9a57c03515479effe40", "/slack/events", app)

@slack_events_adapter.on("url_request")
def handle_message(request):
        app.logger.info(request.method)
        json_dict = json.loads(request.body.decode("utf-8"))
        

@app.route('/', methods=['POST'])
def event_hook():
    incoming_msg = request.values.get('Body', '').lower()
    app.logger.warning(incoming_msg)
    print(incoming_msg, file=sys.stderr)
    resp = "challenge"
    return str(resp)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()

