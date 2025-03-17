from textblob import TextBlob

def analyze_user(api, username):
    """Analyze if a user is larping based on their tweets."""
    try:
        tweets = api.user_timeline(screen_name=username, count=100, tweet_mode="extended")
        tweet_texts = [tweet.full_text for tweet in tweets]
        
        if not tweet_texts:
            return "unknown"
        
        # Sentiment analysis
        polarities = [TextBlob(tweet).sentiment.polarity for tweet in tweet_texts]
        avg_polarity = sum(polarities) / len(polarities)
        variance = len(set([round(p, 1) for p in polarities]))  # Rough measure of inconsistency
        
        # Heuristic: extreme sentiment or high variance might indicate larping
        if abs(avg_polarity) > 0.3 or variance > 5:
            return "larping"
        else:
            return "genuine"
    except tweepy.TweepError as e:
        print(f"Error analyzing {username}: {e}")
        return "unknown"