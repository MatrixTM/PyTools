import asyncio
from asyncio import sleep, Event, create_task
from contextlib import suppress
from getpass import getpass
from itertools import cycle
from os import name, system
from socket import gethostname

from aioconsole import aprint, ainput
from pystyle import Colorate, Colors, Center

import tools
from tools.impl import handle as tools_handle


# noinspection PyMethodMayBeStatic
class Console:
    def __init__(self):
        self.using = None
        self.dots = cycle(["|", "/", "-", "\\"])
        self.loading_text = ""

    async def banner(self):
        await self.clear()
        await aprint(Colorate.Diagonal(Colors.yellow_to_red, Center.XCenter("""
╔════════════════════════════════════════════════════════════════════════════════╗
║    ooooooooo.              ooooooooooooo                     oooo              ║
║    `888   `Y88.             8'   888   `8                     `888             ║
║     888   .d88' oooo    ooo      888       .ooooo.   .ooooo.   888   .oooo.o   ║
║     888ooo88P'   `88.  .8'       888      d88' `88b d88' `88b  888  d88(  "8   ║
║     888           `88..8'        888      888   888 888   888  888  `"Y88b.    ║
║     888            `888'         888      888   888 888   888  888  o.  )88b   ║
║    o888o            .8'         o888o     `Y8bod8P' `Y8bod8P' o888o 8""888P'   ║
║                 .o..P'                                                         ║
║                 `Y8P'                                                          ║
╚═══════════════════════╦═════════════════════════════════╦══════════════════════╝
                        ║   Coded By : MXTeam - V 1.0     ║
                        ╚═════════════════════════════════╝\n\n\n\n""")))

    async def loader(self):
        while 1:
            if not self.using.is_set():
                await self.using.wait()
            await aprint(Colorate.Horizontal(Colors.rainbow,
                            f"[{next(self.dots)}] {self.loading_text}"),
                         end="\r")
            await sleep(.05)

    async def input(self, *messages, hide_value=False):
        if not hide_value:
            return await ainput(' '.join([str(txt) for txt in messages]))
        return getpass(' '.join([str(txt) for txt in messages]))

    async def cinput(self, *messages, hide_value=False):
        return await self.input(Colorate.Horizontal(Colors.yellow_to_red,
                                                    f"╔═══[{gethostname()}@PyTools]"
                                                    f"{(' (' + ' '.join([txt for txt in messages]) + ')') if messages else ''} "
                                                    f"\n╚══════> "), hide_value=hide_value)

    async def error(self, *messages):
        await aprint(Colorate.Diagonal(Colors.red_to_white, "[X] " + ' '.join([str(txt) for txt in messages])))

    async def clear(self):
        if self.using:
            self.using.clear()
            await aprint(' ' * len(self.loading_text), end="\r")
            self.loading_text = ''
        await self.command('cls' if name == 'nt' else 'clear')

    async def run(self):
        self.using = Event()
        create_task(self.loader())
        while 1:
            inp = await self.cinput()
            if not inp:
                pass
            await self.handle(inp.strip())
            self.using.clear()

    async def command(self, cmd):
        with suppress(Exception):
            return await (await asyncio.create_subprocess_shell(cmd=cmd)).communicate()
        system(cmd)

    async def handle(self, inp):
        cmd, args = tools.Patterns.parsecommand(inp)
        cmd = cmd.upper()

        try:
            if {cmd} & {"HELP", "?"}:
                await aprint("help ?")
            elif {cmd} & {"EXIT", "QUIT", "LOGOUT", "EXIT()"}:
                exit(-1)
            elif {cmd} & {"CLEAR", "CLS"}:
                await self.banner()
            elif await tools_handle(self, cmd, *args):
                pass
            elif cmd:
                await self.error(f"\"{cmd.lower()}\" command not found")

        except Exception as e:
            self.using.clear()
            await self.error((str(e) or repr(e)) + ' ' * 50)

    async def info(self, *messages):
        await aprint(Colorate.Diagonal(Colors.blue_to_white, "[!] " + ' '.join([txt for txt in messages])))
