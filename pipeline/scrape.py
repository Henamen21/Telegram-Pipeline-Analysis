# pipeline/scrape.py

import os
import json
import logging
import asyncio
import time
from datetime import datetime
from pathlib import Path
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

DATA_DIR = "data/raw/telegram_messages"
MEDIA_DIR = "data/raw/media"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

logging.basicConfig(filename="scrape.log", level=logging.INFO)

def sanitize(name):
    return name.replace("https://t.me/", "").replace("/", "_")

def save_message_json(channel_name, messages):
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join(DATA_DIR, date_str)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{channel_name}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

async def scrape_channel(client, channel_url):
    channel_name = sanitize(channel_url)
    messages = []

    try:
        async for message in client.iter_messages(channel_url, limit=100):
            await asyncio.sleep(0.2)  # To avoid aggressive behavior

            msg_data = {
                "id": message.id,
                "date": str(message.date),
                "sender_id": message.sender_id,
                "text": message.message,
                "has_media": bool(message.media),
                "media_path": None,
            }

            if isinstance(message.media, MessageMediaPhoto):
                try:
                    media_file = f"{channel_name}_{message.id}.jpg"
                    full_path = os.path.join(MEDIA_DIR, media_file)
                    await client.download_media(message, full_path)
                    msg_data["media_path"] = full_path
                except Exception as e:
                    logging.warning(f"Failed to download media: {e}")

            messages.append(msg_data)

        save_message_json(channel_name, messages)
        logging.info(f"✅ Scraped {len(messages)} messages from {channel_url}")

    except Exception as e:
        logging.error(f"❌ Failed to scrape {channel_url}: {e}")
        print(f"Error scraping {channel_url}: {e}")

async def main():
    client = TelegramClient("scraper_session", api_id, api_hash)
    
    print("🔐 Starting client — you'll be prompted to log in (only once).")
    await client.start()  # Prompts for phone number and code if not logged in

    async with client:
        print("you are inside client")
        for channel in CHANNELS:
            await scrape_channel(client, channel)

    print("✅ Scraping completed.")

if __name__ == "__main__":
    asyncio.run(main())
