import json
from pathlib import Path
#import slacker
from api_tokens import devtoken

#slack = Slacker(devtoken)

path = "logs/actionone/2016-07-19.json"
userspath = "logs/users.json"


# Returns a list of dicts containing messages from a given channel (passed via parameter chan)
def show_messages(chan):
    # Create a list to hold chat data from every file.
    total_chat_data = []
    # Iterate thru chan's directory and retrieve list of files
    chan_dir = Path("./logs/" + chan)
    chan_files = []
    for file in chan_dir.iterdir():
        chan_files.append(str(file))
    # Open users file 
    with open(userspath) as raw_data:
        user_data = json.load(raw_data)
    # Open chat files from the list of paths, and add names for all of them.
    for filepath in chan_files:
        with open(filepath) as raw_data:
            chat_data = json.load(raw_data)
        # Iterate through the messages and assign real names instead of user IDs    
        for msg in chat_data:
            for usr in user_data:
                # Check to see if it's a user's post, or a bot post.
                if 'bot_id' in msg:
                    msg['real_name'] = "bot"
                else:
                    if usr['id'] == msg['user']:
                        # Add the real_name attribute, used to display names
                        # See if the user has a real_name
                        try:
                            msg['real_name'] = usr['real_name']
                        # If not, make it their username
                        except KeyError:
                            msg['real_name'] = usr['name']
                        # Add the user_name attribute, used for mouseover display
                        msg['user_name'] = usr['name']
        for msg in chat_data:
            total_chat_data.append(msg)
        # TODO: Change mentions to real names

        # TODO: Change 'ts' to a printable date
            


    return total_chat_data