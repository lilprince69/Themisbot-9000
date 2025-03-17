from src.auth import get_api
from src.listener import LarpStreamListener
from config.settings import BOT_HANDLE

def main():
    """Start the Larp Bot."""
    print("Starting X Larp Bot...")
    api = get_api()
    bot_handle = BOT_HANDLE
    
    # Print bot's handle for reference
    print(f"Bot handle: @{api.me().screen_name}")
    
    # Start the stream
    listener = LarpStreamListener(api, bot_handle)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(follow=[api.me().id_str])

if __name__ == "__main__":
    main()