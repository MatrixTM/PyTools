from asyncio import sleep, TimeoutError, create_task
from contextlib import suppress
from itertools import cycle
from aiocfscrape import CloudflareScraper

from aioconsole import aprint
from pystyle import Colorate, Colors
from tools import Tool
from re import compile

dots = cycle(["|", "/", "-", "\"])
cfx_regex = compile(u"(?:cfx[.]re/join/|)(\w+)")


class Cfxfinder(Tool):
    using = False

    @staticmethod
    async def run(*args):
        assert len(args) == 1, "bad args"

        cfx_code = cfx_regex.search(args[0].lower())

        assert cfx_code, "The CFX code is not valid"
        cfx_code = cfx_code.group(1)
        assert len(cfx_code) == 6, "The CFX code is not valid"

        try:
            with suppress(KeyboardInterrupt):
                Cfxfinder.using = True
                create_task(Cfxfinder.loader(cfx_code))
                await sleep(.9)
                try:
                    cfx_info = await Cfxfinder.getinfo(cfx_code)
                    await aprint(
                        Colorate.Horizontal(Colors.green_to_cyan,
                                            'Information received from cfx server [%s] {\nAddress: %s\nClients: '
                                            '%s\nLocale: %s\nsvMaxclients: %s\nownerName: %s\n}' % (
                                                cfx_info['name'], cfx_info['host'], cfx_info['clients'],
                                                cfx_info['locale'], cfx_info['maxclients'], cfx_info['ow'])))
                except Exception as e:
                    await aprint(e)
        finally:
            Cfxfinder.using = False

    @staticmethod
    async def getinfo(cfxcode):
        with suppress(TimeoutError):
            async with CloudflareScraper() as s, \
                    s.get('https://servers-frontend.fivem.net/api/servers/single/' + cfxcode) as res:
                assert res.status == 200, f"Status Code :{res.status}" + " " * 50

                cfx_json = await res.json()
                assert "error" not in cfx_json, cfx_json['error'] + " " * 50

                return {
                    'name': cfx_json['Data']['hostname'],
                    'host': cfx_json['Data']['connectEndPoints'][0],
                    'clients': cfx_json['Data']['clients'],
                    'maxclients': cfx_json['Data']['svMaxclients'],
                    'locale': cfx_json['Data']['vars']['locale'],
                    'ow': cfx_json['Data']['ownerName']
                }

    @staticmethod
    async def loader(address):
        while Cfxfinder.using:
            await aprint(
                "[%s] Getting Information From (%s)" %
                (next(dots),
                 "https://cfx.re/join/" + address),
                end="\r")
            await sleep(.05)
