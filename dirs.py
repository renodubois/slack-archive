from pathlib import Path

# Retrieve all of the channel names from the logs folder.
# Takes no parameters, automatically searches the 'logs' folder.
# Returns a list of dicts, for use with the jinja2 templating engine.
def get_chan_info():
    p = Path('./logs')
    chan_names = []
    for f in p.iterdir():
        if f.is_dir() and not str(f)[6] == ".":
            dir_name = str(f)
            dir_path = str(f)
            dir_name = dir_name[5:]
            chan_names.append({'name':dir_name, 'path':dir_path})
    return chan_names