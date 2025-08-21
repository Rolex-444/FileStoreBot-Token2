from aiohttp import web
import threading

async def handle(request):
    return web.Response(text="Bot is alive")

app = web.Application()
app.add_routes([web.get('/', handle)])

def run_webserver():
    web.run_app(app, host='0.0.0.0', port=8080)

def start():
    threading.Thread(target=run_webserver).start()
  
