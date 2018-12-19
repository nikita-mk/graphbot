from botClass import SlackBot
import yaml

with open(<config path>, 'r') as stream:
    try:
        dict = yaml.load(stream)
    except yaml.YAMLError as exc:
        print('Exception!')
mybot = SlackBot(dict)
mybot.start()
