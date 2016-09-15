import json
from api_tokens import devtoken
from pathlib import Path

userspath = "logs/users.json"

'''
    show_messages(chan)
    Shows messages for a given channel.
    Returns: a list of dicts containing messages from a given channel (passed via parameter chan)
'''
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
            # Replaces the mentions with actual names
            # First make sure that the text is an actual string
            if 'text' in msg:
                if type(msg['text']) is not None:
                    if 'subtype' in msg:
                        msg['text'] = mentions_to_names(msg['text'], msg['subtype'])
                    else:
                        msg['text'] = mentions_to_names(msg['text'], "")
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
            if 'text' in msg:
                if msg['text'] is not None:
                    total_chat_data.append(msg)
        # TODO: Change mentions to real names
        # TODO: Change 'ts' to a printable date
    return total_chat_data

'''
    mentions_to_names(msg, msg_type)
    Takes a message and message type and replaces any mentions with readble text.
    If the msg_type matches any of the bad_types listed, just returns an empty string.
    Returns: a string containing the message after mentions being replaced
'''
def mentions_to_names(msg, msg_type):
    # A tuple of the types we want to ignore.
    bad_types = ('channel_join', 'pinned_item', 'channel_name', )
    # If the message has some type we don't want to deal with right now, so just remove them.
    if not msg_type == "":
        return ""
    # Length of a 'mention string' (includes '<', '>', the @ and the User ID) minus 1, since we're already counting for
    # the '<'.
    mention_len = 12
    # Make a list for "replace data", used to replace the user ids at the end of the function.
    replace_data = []
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
                # Append the data (user id and index) of the mention to be replaced so that we can iterate through them later
                replace_data.append((i, user_id))
    # We have info regarding the stuff needing to be replaced, go through and replace it.
    for msg_data in reversed(replace_data):
        msg = msg[:msg_data[0]] + '@' + id_to_realname(msg_data[1]) + msg[(msg_data[0]+mention_len):]
    # Return the replaced message.
    return msg


''' 
    id_to_realname(user_id)
    Takes a string containing a user_id, returns the real name or name of the user, depending on availability.
    Returns: a string containing real name or username
'''
def id_to_realname(user_id):
    with open(userspath) as raw_data:
        user_data = json.load(raw_data)
    for usr in user_data:
        if usr['id'] == user_id:
            if 'real_name' in usr:
                return usr['real_name']
            else:
                return usr['name']