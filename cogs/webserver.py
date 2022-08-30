import json
import os

from aiohttp import web
from discord.ext import commands, tasks

app = web.Application()
routes = web.RouteTableDef()


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_server.start()

        @routes.get("/")
        async def welcome(request):
            return web.Response(text="Hello, world")

        @routes.get("/keys")
        async def get_keys(request):
            with open("./api_keys.json") as f:
                keys = json.load(f)
            return web.json_response(keys)

        @routes.post("/keys")
        async def post_keys(request):
            data = await request.post()
            try:
                discord_id = data["discord_id"]
                src_id = data["src_id"]
            except KeyError:
                return 400
            with open("./api_keys.json", "r") as f:
                keys = json.load(f)
                keys[discord_id] = src_id
            with open("./api_keys.json", "w") as f:
                json.dump(keys, f, indent=4)
            return web.json_response(keys)

        self.webserver_port = os.environ.get("PORT", 5000)
        app.add_routes(routes)

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Webserver(bot))
