from bot import Bot
import pyrogram.utils
from webserver import start_webserver
import asyncio

print("Bot is starting...")

pyrogram.utils.MIN_CHANNEL_ID = -1002297453351

async def main():
    await asyncio.gather(
        start_webserver(),
        Bot().start()
    )

if __name__ == "__main__":
    asyncio.run(main())
  
