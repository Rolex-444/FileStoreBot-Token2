from bot import Bot
import pyrogram.utils
import webserver             # <--- Add this line

pyrogram.utils.MIN_CHANNEL_ID = -1002297453351

webserver.start()            # <--- Add this line to start the web server

Bot().run()
