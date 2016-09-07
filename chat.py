import json
#import slacker
from api_tokens import devtoken

#slack = Slacker(devtoken)

path = "090416/actionone/2016-07-19.json"
userspath = "090416/users.json"

def show_messages():
    # Open users file 
    with open(userspath) as raw_data:
        user_data = json.load(raw_data)
    # Open chat file and get the contents
    with open(path) as raw_data:
        chat_data = json.load(raw_data)

    # Make a tuple for easier iteration.
    data = (user_data, chat_data)
    for msg in chat_data:
        for usr in user_data:
            # Giving the messages the real_name attribute to display the real names.
            if usr['id'] == msg['user']:
                # Add the real_name attribute, used to display names
                msg['real_name'] = usr['real_name']
                # Add the user_name attribute, used for mouseover display
                msg['user_name'] = usr['name']
        # TODO: Change mentions to real names
            


    return chat_data

    #return nil