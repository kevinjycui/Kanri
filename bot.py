from flask import Flask, request, Response
import requests
from twilio.twiml.messaging_response import MessagingResponse
from processor import respond
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter("20f2f470e8cee9a57c03515479effe40", "/slack/events", app)

@slack_events_adapter.on("url_request")
def handle_message(request):
        app.logger.info(request.method)
        json_dict = json.loads(request.body.decode("utf-8"))
        

@app.route('/')
def event_hook(request):
    app.logger.info(request.method)
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}
    return

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()

