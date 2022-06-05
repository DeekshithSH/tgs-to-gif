from aiohttp import web
from TGBot.bot import Bot


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response(
        {

            "telegram_bot": "@" + Bot.username
        }
    )
