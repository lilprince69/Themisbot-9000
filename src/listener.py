import tweepy
from src.analyzer import analyze_user
from src.response import generate_response

class LarpStreamListener(tweepy.StreamListener):
    """Listens for mentions and processes them."""
    def __init__(self, api, bot_handle):
        self.api = api
        self.bot_handle = bot_handle

    def on_status(self, status):
        if status.in_reply_to_screen_name == self.bot_handle:
            query = status.text
            username = self.extract_username(query)
            if username:
                try:
                    analysis = analyze_user(self.api, username)
                    response = generate_response(username, analysis)
                    self.api.update_status(
                        status=response,
                        in_reply_to_status_id=status.id,
                        auto_populate_reply_metadata=True
                    )
                    print(f"Replied to {status.user.screen_name}: {response}")
                except Exception as e:
                    print(f"Error processing {query}: {e}")
            else:
                print(f"No valid username in query: {query}")

    def extract_username(self, query):
        """Extract target username from query."""
        import re
        pattern = r'@([a-zA-Z0-9_]+)'
        matches = re.findall(pattern, query)
        return matches[1] if len(matches) > 1 else None