# Small helper functions
# -----------------------
import json


def pp(print_me_pretty):
    json_pretty = json.dumps(print_me_pretty, sort_keys=True, indent=2, separators=(',', ': '))
    return json_pretty




