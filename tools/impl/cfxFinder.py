from asyncio import sleep, TimeoutError
from contextlib import suppress
from aiocfscrape import CloudflareScraper

from aioconsole import aprint
from pystyle import Colorate, Colors
from tools import Tool
from re import compile

cfx_regex = compile(u"(?:cfx[.]re/join/|)(\w+)")


class Cfxfinder(Tool):
    @staticmethod
    async def run(console, *args):
        assert len(args) == 1, "Usage: cfx <Cfx_Code>"

        cfx_code = cfx_regex.search(args[0].lower())

        assert cfx_code, "The CFX code is not valid"
        cfx_code = cfx_code.group(1)
        assert len(cfx_code) == 6, "The CFX code is not valid"

        with suppress(KeyboardInterrupt):
            console.using.set()
            console.loading_text = "Getting Information From (%s)" % ("https://cfx.re/join/" + cfx_code)
            await sleep(.9)

            cfx_info = await Cfxfinder.getinfo(cfx_code)

            await aprint(
                Colorate.Horizontal(Colors.green_to_cyan,
                                    'Information received from cfx server [%s] {\nAddress: %s\nClients: '
                                    '%s\nLocale: %s\nsvMaxclients: %s\nownerName: %s\n}' % (
                                        cfx_info['name'], cfx_info['host'], cfx_info['clients'],
                                        cfx_info['locale'], cfx_info['maxclients'], cfx_info['ow'])))

    @staticmethod
    async def getinfo(cfxcode):
        with suppress(TimeoutError):
            async with CloudflareScraper() as s, \
                    s.get('https://servers-frontend.fivem.net/api/servers/single/' + cfxcode) as res:
                assert res.status == 200, f"Status Code :{res.status}"

                cfx_json = await res.json()
                assert "error" not in cfx_json, cfx_json['error']

                return {
                    'name': cfx_json['Data']['hostname'],
                    'host': cfx_json['Data']['connectEndPoints'][0],
                    'clients': cfx_json['Data']['clients'],
                    'maxclients': cfx_json['Data']['svMaxclients'],
                    'locale': cfx_json['Data']['vars']['locale'],
                    'ow': cfx_json['Data']['ownerName']
                }
