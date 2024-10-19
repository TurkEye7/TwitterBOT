import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Set up Twitter API client
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
twitter_api = tweepy.API(auth)

# WOEID (Where on Earth IDentifier) for trending topics
# You can use WOEID 1 for worldwide trends, or find a specific location's WOEID
WOEID = 1  # Worldwide

def fetch_trending_topics():
    try:
        trends = twitter_api.get_place_trends(id=WOEID)
        trending_topics = [trend['name'] for trend in trends[0]['trends']]
        return trending_topics[:5]  # Get the top 5 trending topics
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []

def post_tweet(message):
    try:
        twitter_api.update_status(status=message)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    # Fetch trending topics
    trending_topics = fetch_trending_topics()

    # If we have any trending topics, post a tweet
    if trending_topics:
        tweet_message = f"Trending Now: {', '.join(trending_topics)}. #Trending #News"
        post_tweet(tweet_message)
    else:
        print("No trending topics available.")
