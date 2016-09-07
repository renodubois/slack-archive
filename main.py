import json
import argparse
#import slacker
from api_tokens import devtoken

#slack = Slacker(devtoken)

# Create our parser, and specify some arguments
#parser = argparse.ArgumentParser(description="Displays chat data from a Slack .json file ")
#parser.add_argument('path', metavar='-p')
# Grab our chat log from the folder it is in

path = "090416/actionone/2016-07-19.json"
userspath = "090416/users.json"

# Open users file 
with open(userspath) as raw_data:
    user_data = json.load(raw_data)
# Open chat file and get the contents
with open(path) as raw_data:
    chat_data = json.load(raw_data)

# Make a tuple for easier iteration.
data = (user_data, chat_data)

# Giving the messages the real_name attribute to display.
for msg in chat_data:
    for usr in user_data:
        if usr['id'] == msg['user']:
            msg['real_name'] = usr['real_name']

for msg in chat_data:
    print(msg['real_name'] + ": " + msg['text'])