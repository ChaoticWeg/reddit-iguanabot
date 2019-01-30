from lib import reddit, data

from dotenv import load_dotenv

import os, random, praw

def pick_iguana():
    iguanas = data.load_json('data/iguanas.json')
    return random.choice(iguanas)

def build_footer():
    footers = data.load_json('data/footers.json')
    this_footer = random.choice(footers)
    return f"\n\n---\n\n^(I am a bot, and this comment was submitted automatically.)  \n^({this_footer})"

def run():
    bot = reddit.get_reddit()
    assert bot.user.me() is not None, "bot.user.me() is None; read-only mode?"

    subreddit = bot.subreddit(os.getenv('subreddit'))
    print(subreddit)

    known_threads = data.load_json('data/known_threads.json')
    if known_threads is None:
        known_threads = []

    for submission in subreddit.new():
        should_post = True

        if "Game Thread" in submission.title and not submission.id in known_threads:
            # double-check that we have not already posted an iguana here, and add to known threads if we have
            for comment in submission.comments:
                if comment.author.id == bot.user.me().id:
                    print(f"Found game thread {submission.id} but I've already posted there! Making note...")

                    should_post = False
                    if not submission.id in known_threads:
                        known_threads.append(submission.id)
                    break

            if not should_post:
                continue

            iguana = pick_iguana()
            footer = build_footer()
            message = f"Pre-game iguana: {iguana}{footer}"

            try:
                submission.reply(message)
            except praw.exceptions.APIException as e:
                print(f"APIException while posting iguana to {submission.id}: {e}")
            except Exception as e:
                print(f"Unknown exception while posting iguana to {submission.id}: {e}")
            
            known_threads.append(submission.id)
    
    data.dump_json('data/known_threads.json', known_threads)

if __name__ == "__main__":
    load_dotenv()

    assert os.getenv('praw_site') is not None, "specify praw_site in .env or environment"
    assert os.getenv('subreddit') is not None, "specify subreddit in .env or environment"

    run()
