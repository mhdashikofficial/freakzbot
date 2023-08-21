import asyncio
import requests
from telegram import Bot

# Your Telegram Bot API token
BOT_TOKEN = 'your_bot_token_here'

# List of group chat IDs where the bot is a member
GROUP_CHAT_IDS = [123456789, 987654321]

# Channel username or ID from which to get updates
CHANNEL_USERNAME = '@your_channel_username'

# Initialize the Telegram bot
bot = Bot(token=BOT_TOKEN)

# Function to send video to groups
async def send_video_to_groups(video_url):
    for chat_id in GROUP_CHAT_IDS:
        try:
            # Send the video to the group
            bot.send_video(chat_id=chat_id, video=video_url)
            print(f"Sent video to group {chat_id}")
        except Exception as e:
            print(f"Error sending video to group {chat_id}: {e}")

# Function to delete a message
async def delete_message(chat_id, message_id):
    await asyncio.sleep(600)  # Sleep for 10 minutes
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"Deleted message {message_id} from group {chat_id}")
    except Exception as e:
        print(f"Error deleting message {message_id} from group {chat_id}: {e}")

# Main function
async def main():
    offset = None
    while True:
        try:
            response = bot.get_updates(offset=offset)
            for update in response['result']:
                if 'message' in update and 'video' in update['message']:
                    video_url = update['message']['video']['file_id']
                    asyncio.create_task(send_video_to_groups(video_url))
                    asyncio.create_task(delete_message(update['message']['chat']['id'], update['message']['message_id']))
                offset = update['update_id'] + 1
        except Exception as e:
            print(f"Error getting updates: {e}")
        await asyncio.sleep(1)

# Run the event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
