from aiohttp import web
import asyncio

async def handle(request):
    return web.Response(text="Bot is alive")

app = web.Application()
app.add_routes([web.get('/', handle)])

async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    print("Webserver started at http://0.0.0.0:5000/")

# To run this as part of your main program, you would do:
if __name__ == "__main__":
    asyncio.run(start_webserver())
    
  
