import sys
import time

def start(self):
        if self.slack_client.rtm_connect():
            print("Bot is alive and listening for messages...")
            while True:
                events = self.slack_client.rtm_read()
                for event in events:
                    if event.get('type') == 'message':
                        self.on_message(event)
                time.sleep(1)
        else:
            print('Connection failed, invalid token?')
            sys.exit(1)