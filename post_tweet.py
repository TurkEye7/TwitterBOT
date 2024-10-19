import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Set up OAuth1a Authentication
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, 
    TWITTER_API_SECRET, 
    TWITTER_ACCESS_TOKEN, 
    TWITTER_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Post a tweet
tweet_content = "Hello, world! This is a test tweet from my bot."
try:
    api.update_status(tweet_content)
    print("Tweet posted successfully!")
except tweepy.errors.Forbidden as e:
    print(f"Error posting tweet (Forbidden): {e}")
except tweepy.TweepyException as e:
    print(f"General error: {e}")
