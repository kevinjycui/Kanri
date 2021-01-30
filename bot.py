from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from processor import respond
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter("20f2f470e8cee9a57c03515479effe40", "/slack/events", app)
@slack_events_adapter.on("challenge")
def catchChallenge(challenge_data):
	return(challenge_data.challenge)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respond(incoming_msg))
    return str(resp)

if __name__ == '__main__':
    app.run()

