# Import Bottle modules.
from bottle import (app, Bottle, get, post, response, request, route, run, jinja2_view,
redirect, static_file)
# System libaries
import json

# Local imports
import chat
import dirs
# api_tokens contains the unique Slack API tokens used to access the API if needed.
from api_tokens import devtoken

@get("/")
@jinja2_view("templates/main_menu.html")
def main_menu():
    # Grabs the names of all the folders in the logs directory, to be displayed on the main menu.
    channels = dirs.get_chan_names()
    #channels = [{ 'name':"actionone" }]
    return { 'channels':channels }

@get("/<chan>/")
@jinja2_view("templates/chat.html")
def chan_msg(chan):
    chat_data = chat.show_messages(chan)
    return { 'chat_log':chat_data }



slack_chat = app()
#slack_chat = SessionMiddleware(slack_chat)

if __name__ == "__main__":
    run(app = slack_chat, host = "localhost", port = 80)
