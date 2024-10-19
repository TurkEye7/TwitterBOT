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

# Test the authentication by retrieving the authenticated user's details
try:
    user = api.verify_credentials()
    print(f"Authenticated as: {user.screen_name}")
except tweepy.TweepError as e:
    print(f"Error: {e}")
