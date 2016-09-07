from bottle import (app, Bottle, get, post, response, request, route, run, jinja2_view,
redirect, static_file)

import json
import chat
from api_tokens import devtoken

@get("/")
@jinja2_view("templates/main_menu.html")
def main_menu():
    # List used for testing purposes.
    channels = [{ 'name':"actionone" }]
    return { 'channels':channels }

@get("/actionone/")
@jinja2_view("templates/chat.html")
def show_a1_msg():
    chat_data = chat.show_messages()
    return { 'chat_log':chat_data }



slack_chat = app()
#slack_chat = SessionMiddleware(slack_chat)

if __name__ == "__main__":
    run(app = slack_chat, host = "localhost", port = 80)
