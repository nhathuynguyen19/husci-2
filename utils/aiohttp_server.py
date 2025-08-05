import os
from aiohttp import web

async def head_handler(request):
    return web.Response(status=200)

async def get_handler(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_head("/", head_handler)
app.router.add_get("/", get_handler)

web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
