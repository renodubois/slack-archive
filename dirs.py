from pathlib import Path

# Retrieve all of the channel names from the logs folder.
# Takes no parameters, automatically searches the 'logs' folder.
# Returns a list of dicts, for use with the jinja2 templating engine.
def get_chan_names():
    p = Path('./logs')
    chan_names = []
    for f in p.iterdir():
        if f.is_dir():
            dir_name = str(f)
            dir_name = dir_name[5:]
            chan_names.append({'name':dir_name})

    return chan_names