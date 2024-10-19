import os
import tweepy
import schedule
import time
from dotenv import load_dotenv
import random

# Load environment variables
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

# Notable figures and official accounts in MENA region
figures = [
    "Hassan Sheikh Mohamud", "Mohamed Bin Salman", "Abdel Fattah el-Sisi", 
    "Emmanuel Macron", "Recep Tayyip Erdoğan", "King Abdullah II", 
    "Crown Prince Mohamed Bin Zayed", "Bashar al-Assad", "Kais Saied",
    "@HassanSMohamud", "@MbS", "@KingSalman", "@AlsisiOfficial", "@KingAbdullahII"
]

# Additional keywords related to politics, military, and government in Arabic and English
keywords = ["politics", "government", "military", "الجيش", "الحكومة", "سياسة"]

# Function to fetch relevant tweets
def fetch_relevant_tweets():
    print("Fetching relevant tweets...")
    # Randomly select a notable figure or keyword for the search query
    query = f"{random.choice(figures)} OR {random.choice(keywords)} -filter:retweets"
    try:
        # Search tweets in English and Arabic
        tweets = twitter_api.search_tweets(q=query, lang="ar", count=5, tweet_mode="extended") + \
                 twitter_api.search_tweets(q=query, lang="en", count=5, tweet_mode="extended")
        print(f"Found {len(tweets)} tweets.")
        return tweets
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# Function to repurpose and post tweets
def repurpose_and_post_tweet():
    print("Repurposing and posting a tweet...")
    tweets = fetch_relevant_tweets()
    if tweets:
        for tweet in tweets:
            try:
                # Repackage the tweet and give credit
                original_text = tweet.full_text
                user = tweet.user.screen_name
                repackaged_text = f"📢 {original_text} \n\nSource: @{user} #MiddleEast #NorthAfrica"

                # Post the tweet
                twitter_api.update_status(status=repackaged_text)
                print("Tweet posted successfully!")

                # Limit to 1 post per call to manage frequency
                break
            except Exception as e:
                print(f"Error posting tweet: {e}")
    else:
        print("No tweets available to repurpose.")

# For immediate testing
if __name__ == "__main__":
    print("Starting the bot...")
    print("Testing immediate tweet posting...")
    repurpose_and_post_tweet()
