import asyncio
import os
from aiohttp import web

async def head_handler(request):
    return web.Response(status=200)

app = web.Application()
app.router.add_head("/", head_handler)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
