import random

def pick_random(arr):
    try:
        return random.choice(arr)
    except KeyError:
        return None
