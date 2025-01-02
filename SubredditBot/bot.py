import praw
import time
import random

# List of subreddits where you might want to post
subreddits = ["", "", ""]

# Single message to use
message = ""

# Set up Reddit API connection
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent='python:ricky:v1.0 (by /u/)'
)

# Post to subreddits with rate limiting in mind
for subreddit in subreddits:
    try:
        subreddit_instance = reddit.subreddit(subreddit)
        subreddit_instance.subscribe()  # Join the subreddit
        
        # Post a comment on the top post
        for submission in subreddit_instance.hot(limit=1):  # Adjust the limit as needed
            submission.reply(message)
            print(f"Posted to {subreddit}: {message}")
            
            # Sleep to avoid rate limiting
            time.sleep(random.randint(600, 900))  # Random delay between 10-15 minutes
    except praw.exceptions.RedditAPIException as e:
        print(f"An error occurred in subreddit {subreddit}: {e}")
        if "RATELIMIT" in str(e):
            delay = int(e.message.split(" ")[-2]) * 60  # Extract recommended wait time
            print(f"Rate limit hit. Waiting for {delay} seconds.")
            time.sleep(delay)
    except Exception as e:
        print(f"An unexpected error occurred in subreddit {subreddit}: {e}")
        time.sleep(300)  # Sleep for 5 minutes to recover
