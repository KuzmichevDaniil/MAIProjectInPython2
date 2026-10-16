import json
import os

from streamstats.errors import FileExists

def make_report(stats, arg):
    if os.path.exists(str(arg)):
        raise FileExists(arg)
    else:
        with open(arg, 'w', encoding='utf-8') as file:
            json.dump(stats, file, indent=4, ensure_ascii=False)
        