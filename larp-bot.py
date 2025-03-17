import tweepy
import os
import re
from textblob import TextBlob

# Load X API credentials from environment variables
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Authenticate with X
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to extract target username from query
def extract_username(query):
    pattern = r'@([a-zA-Z0-9_]+)'
    matches = re.findall(pattern, query)
    # Skip the AI's handle (first match), get target user (second match)
    return matches[1] if len(matches) > 1 else None

# Function to analyze if a user is larping
def analyze_user(username):
    try:
        # Fetch user's last 100 tweets
        tweets = api.user_timeline(screen_name=username, count=100, tweet_mode="extended")
        tweet_texts = [tweet.full_text for tweet in tweets]
        
        # Analyze sentiment for signs of larping
        polarities = [TextBlob(tweet).sentiment.polarity for tweet in tweet_texts]
        avg_polarity = sum(polarities) / len(polarities) if polarities else 0
        
        # Rough heuristic: extreme or varied sentiment might mean larping
        if abs(avg_polarity) > 0.3 or len(set(polarities)) > 5:
            return "larping"
        else:
            return "genuine"
    except tweepy.TweepError as e:
        print(f"Error fetching tweets for {username}: {e}")
        return "unknown"

# Function to generate a sassy response with personality
def generate_response(username, analysis):
    if analysis == "larping":
        return f"@{username} is larping harder than a D&D nerd on a Saturday night. Total fraud, and I’m calling it!"
    elif analysis == "genuine":
        return f"@{username}’s the real deal. No larp here—just painfully authentic."
    else:
        return f"@{username}? Couldn’t figure ‘em out. Probably too sneaky for me."

# Stream listener to handle incoming mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Replace "YourAI" with your AI's actual X handle
        if status.in_reply_to_screen_name == "YourAI":
            query = status.text
            username = extract_username(query)
            if username:
                try:
                    analysis = analyze_user(username)
                    response = generate_response(username, analysis)
                    api.update_status(
                        status=response,
                        in_reply_to_status_id=status.id,
                        auto_populate_reply_metadata=True
                    )
                    print(f"Replied to {status.user.screen_name}: {response}")
                except Exception as e:
                    print(f"Error processing {query}: {e}")
            else:
                print(f"No valid username in query: {query}")

# Main function to start the bot
def main():
    print("Starting Larp Bot...")
    # Get your AI's user ID for the stream
    my_id = api.me().id_str
    print(f"Bot handle: @{api.me().screen_name}")
    
    # Start the stream
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(follow=[my_id])

if __name__ == "__main__":
    main()