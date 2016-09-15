# Library imports
from jinja2 import Environment, PackageLoader
from pathlib import Path
from os import remove, mkdir, path, getcwd
from shutil import rmtree
# local imports
import chat
import dirs


env = Environment(loader = PackageLoader("chat", "templates"))

index_template = env.get_template("main_menu.html")
chat_template = env.get_template("chat.html")


logs_dir = Path("./logs/")
chan_info = dirs.get_chan_info()

# Cleanup previous files
if path.isfile('index.html'):
    remove('index.html')
if path.isdir('chans/'):
    rmtree('chans/')
mkdir('chans/')

# Get the 'full' working directory, so local HTML links can be clicked.
cwd = getcwd()
for chan in chan_info:
    chan['full_path'] = cwd + '/chans/' + chan['name'] + '.html'
    print(chan['full_path'])

# Make an index file.
with open('index.html', 'a+') as f:
    f.write(index_template.render({ 'channels':chan_info }))

# Call show messsages for each channel, write them to a html file that is named after that channel.
# Put them in a subdirectory, so it's a little less confusing.
for chan in chan_info:
    with open('chans/{}.html'.format(chan['name']), 'a+') as f:
        chat_data = chat.show_messages(chan['name'])
        f.write(chat_template.render({ 'chat_log':chat_data }))

