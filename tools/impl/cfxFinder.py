import asyncio
from contextlib import suppress
from itertools import cycle
from requests import get, Session
from cfscrape import create_scraper, get_tokens
from json import loads

import aioconsole
from pystyle import Colorate, Colors
from tools import Tool

dots = cycle(["|", "/", "-", "\\"])

session = Session()
session.headers = ...
s = create_scraper(sess=session)

class cfxFinder(Tool):
    using = False

    @staticmethod
    async def run(*args):
        assert len(args) == 1, "bad args"

        cfxCode = str(args[0].lower()).replace('http://', '').replace('https://', '').replace('cfx.re/join/', '')

        assert len(cfxCode) == 6, "The CFX code is not valid"
        with suppress(KeyboardInterrupt):
            cfxFinder.using = True
            asyncio.create_task(cfxFinder.loader(cfxCode))

            try:
                cfxInfo = await cfxFinder.GetInfo(cfxCode)
                if cfxInfo['name']:
                    await aioconsole.aprint(
                        Colorate.Horizontal(Colors.green_to_cyan,
                                            "Information received from cfx server [%s] {\nAddress: %s" % (cfxInfo['name'], cfxInfo['host'])))
                else:
                    await aioconsole.aprint(Colorate.Horizontal(Colors.red_to_purple, cfxInfo))
            except Exception as e:
                await aioconsole.aprint(e)

            cfxFinder.using = False

    @staticmethod
    async def GetInfo(cfxCode):

        with suppress(asyncio.TimeoutError), s.get('https://servers-frontend.fivem.net/api/servers/single/' + cfxCode) as res:
            if res.status_code == 200:
                cfxJson = loads(res.text)
                return {
                    'name': cfxJson['Data']['hostname'],
                    'host': cfxJson['Data']['connectEndPoints'][0]
                }
            else:
                return f"Status Code :{res.status_code}"


    @staticmethod
    async def loader(address):
        while cfxFinder.using:
            await aioconsole.aprint(
                "[%s] Getting Information From (%s)" %
                (next(dots),
                 "https://cfx.re/join/" + address),
                end="\r")
            await asyncio.sleep(.05)
