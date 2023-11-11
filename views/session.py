import discord
import asyncio
from aiohttp import web
from typing import Callable

from modules.errors import HttpException
from modules.githubOauth2 import GithubOAuth2, Scope
from utils.getConfig import get_config


routes = web.RouteTableDef()
bot: discord.Client

parser = get_config()
oauth2_client = GithubOAuth2(
    client_id=parser.get('Github', 'client_id'),
    client_secret=parser.get('Github', 'client_secret')
)


@routes.get('/login/github')
async def github_login(request: web.Request):
    state = request.rel_url.query.get('state')
    return web.HTTPFound(
        oauth2_client.authorize(
            redirect_uri="https://" + request.host + "/login/callback",
            scope=[Scope.user],
            state=state
        )
    )


@routes.get('/login/callback')
async def github_login_callback(request: web.Request):
    state = request.rel_url.query.get('state')
    code = request.rel_url.query.get('code')
    if code is None or state is None:
        return web.HTTPForbidden()

    # Circuital Issue: Session and connector has to use same event loop
    oauth2_client.requests.loop = bot.loop

    try:
        access_token = await oauth2_client.token(
            code=code
        )
    except HttpException as error:
        return web.Response(body={
            "title": error.data.get("error"),
            "message": error.data.get("error_description"),
            "process": "Access Token"
        }, status=error.response_code)

    if access_token.access_token == "":
        return web.HTTPFound("https://" + request.host + "/login/github",)

    event = "login_success"
    listeners: list[tuple[asyncio.Future, Callable[..., bool]]] = getattr(bot, "_listeners", {}).get(event)

    # Dispatch (coroutine)
    if listeners is not None:
        removed = []
        for i, (future, condition) in enumerate(listeners):
            if future.cancelled():
                removed.append(i)
                continue

            try:
                result = condition(state, access_token)
            except Exception as exc:
                future.set_exception(exc)
                removed.append(i)
            else:
                if result:
                    future.set_result((state, access_token))
                    removed.append(i)

        if len(removed) == len(listeners):
            getattr(bot, "_listeners", {}).pop(event)
        else:
            for idx in reversed(removed):
                del listeners[idx]

    try:
        coroutine = getattr(bot, "on_" + event)
    except AttributeError:
        pass
    else:
        await coroutine(state, access_token)
    return web.Response(body="성공적! 페이지를 닫습니다.")
