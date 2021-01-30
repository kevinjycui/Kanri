from slackclient import SlackClient
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClientHandler:
    def __init__(self, token):
        self.client = SlackClient(token)
        self.webclient = WebClient(token=token)

    def list_channels(self):
        channels_call = self.client.api_call("conversations.list")
        if channels_call.get('ok'):
            return channels_call['channels']
        return None

    def send_message(self, message, channel='#general'):
        try:
            response = self.webclient.chat_postMessage(
                channel=channel,
                text=message)
            assert response['message']['text'] == message
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response['ok'] is False
            assert e.response['error']  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()
    SLACK_TOKEN = os.getenv('SLACK_API_TOKEN')

    clientHandler = SlackClientHandler(SLACK_TOKEN)
    channels = clientHandler.list_channels()

    if channels:
        print('Channels: ')
        for c in channels:
            print(c['name'] + ' (' + c['id'] + ')')
    else:
        print('Unable to authenticate.')

    clientHandler.send_message('Hello world', '#general')