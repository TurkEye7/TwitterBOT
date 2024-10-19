import os
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Set up Twitter API client for posting tweets
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
twitter_api = tweepy.API(auth)

# Create the stream listener using the new StreamingClient class
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Only process if the tweet is in English or Arabic
            if tweet.lang in ['en', 'ar']:
                tweet_text = tweet.text
                user_id = tweet.author_id
                # Get the username based on the user ID
                user = twitter_api.get_user(user_id=user_id).screen_name
                repackaged_text = f"🔴 {tweet_text} \n\nSource: @{user} #MiddleEast #NorthAfrica"
                
                # Post the tweet
                twitter_api.update_status(status=repackaged_text)
                print("Tweet posted successfully!")
        except Exception as e:
            print(f"Error posting tweet: {e}")

    def on_errors(self, errors):
        print(f"Error received: {errors}")

if __name__ == "__main__":
    print("Starting the bot...")

    # Instantiate the stream listener
    bearer_token = TWITTER_BEARER_TOKEN
    stream_listener = MyStreamListener(bearer_token)

    # Add rules to track specific keywords and official accounts
    rules = [
        tweepy.StreamRule("Hassan Sheikh Mohamud OR Mohamed Bin Salman OR politics OR government OR military"),
        tweepy.StreamRule("Middle East OR North Africa OR حكومة OR سياسة OR الجيش")
    ]

    # Add rules to the stream
    stream_listener.add_rules(rules, dry_run=False)

    # Start streaming
    stream_listener.filter(tweet_fields=["lang"])
