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
            if 'text' in msg and type(msg['text']) is not None:
                    #print(type(msg['text']))
                    #print(msg['text'])
                    msg['text'] = mentions_to_names(msg['text'], "")
            for usr in user_data:
                # Replaces the mentions with actual names
                # First make sure that the text is an actual string
                
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

def mentions_to_names(msg, msg_type):
    # Length of a 'mention string' (includes '<', '>', the @ and the User ID) minus 1, since we're already counting for
    # the '<'.
    mention_len = 12
    # Open user files to get User Data
    with open(userspath) as raw_data:
        user_data = json.load(raw_data)
    # Go through the message until we find a '<' character
    for i in range(len(msg)):
        # If we find a '<' char, we know that we have a @ then a User ID, then a '>'
        # We can use the defined len of the user ID to replace the mention with a real name
        if msg[i] == '<':
            # If we have a '@' after the '<', it's a user being mentioned.
            if msg[i+1] == '@':
                user_id = msg[(i+2):(i+(mention_len-1))]
                # If this message is referencing someone joining the channel, then the length is different.
                if msg_type == 'channel_join':
                    return ""
                # Replace the .json mention with readable text.
                print(msg[:i])
                print(id_to_realname(user_id))    
                new_msg = msg[:i] + '@' + id_to_realname(user_id) + msg[(i+mention_len):]
                return new_msg
    return msg


def id_to_realname(user_id):
    with open(userspath) as raw_data:
        user_data = json.load(raw_data)
    for usr in user_data:
        if usr['id'] == user_id:
            if 'real_name' in usr:
                return usr['real_name']
            else:
                return usr['name']