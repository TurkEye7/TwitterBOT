import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter Bearer Token
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Test URL - using the "GET /2/tweets/search/recent" endpoint to verify the token
url = "https://api.twitter.com/2/tweets/search/recent"

# Parameters for the search query (use a simple query term like "Twitter")
params = {
    "query": "Twitter",
    "max_results": 10
}

# Headers with Bearer Token
headers = {
    "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
}

# Make a GET request to verify the token
response = requests.get(url, headers=headers, params=params)

# Check the response
if response.status_code == 200:
    print("Bearer Token is valid!")
    data = response.json()
    print("Sample Tweets:")
    for tweet in data.get("data", []):
        print(f"- {tweet['text']}")
else:
    print(f"Error: {response.status_code} - {response.json()}")
