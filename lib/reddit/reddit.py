import praw, os

GAME_THREAD_INDICATOR = "[Game Thread]"

def __get_user_agent():
    is_prod = os.getenv('prod_env')
    version = "prod" if is_prod else "dev"
    return f"Dallas Stars GDT IguanaBot by /u/ChaoticWeg with apologies to /u/OrganicRedditor ({version})"

def get_reddit():
    return praw.Reddit(user_agent=__get_user_agent())
