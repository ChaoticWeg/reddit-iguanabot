import json

def load_json(filename):
    contents = None
    try:
        with open(filename, 'r') as infile:
            contents = json.load(infile)
    except:
        pass
    return contents

def dump_json(filename, data, **kwargs):
    try:
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, sort_keys=False, indent=4, **kwargs)
    except Exception as e:
        print(f"Exception caught while dumping data to {filename}: {e}")
