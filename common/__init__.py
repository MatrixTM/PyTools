import asyncio
from os import name, system
from socket import gethostname

from aioconsole import aprint, ainput
from pystyle import Colorate, Colors, Center

import tools
from tools.impl import handle as tools_handle


class Console:
    @staticmethod
    async def banner():
        await Console.clear()
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

    @staticmethod
    async def input(*messages):
        return await ainput(' '.join([txt for txt in messages]))

    @staticmethod
    async def error(*messages):
        await aprint(Colorate.Diagonal(Colors.red_to_white, "[X] " + ' '.join([txt for txt in messages])))

    @staticmethod
    async def clear():
        await Console.command('cls' if name == 'nt' else 'clear')

    @staticmethod
    async def run():
        while 1:
            inp = (await Console.input(Colorate.Horizontal(Colors.yellow_to_red,
                                                                  f"╔═══[{gethostname()}"
                                                                  f"@PyTools]\n╚══════> ")))
            if not inp: pass
            await Console.handle(inp.strip())

    @staticmethod
    async def command(cmd):
        try:
            return await (await asyncio.create_subprocess_shell(cmd=cmd)).communicate()
        except:
            system(cmd)

    @staticmethod
    async def handle(inp):
        cmd, args = tools.Patterns.parseCommand(inp)
        cmd = cmd.upper()

        try:
            if {cmd} & {"HELP", "?"}:
                await aprint("help ?")
            elif {cmd} & {"EXIT", "QUIT", "LOGOUT", "EXIT()"}:
                exit(-1)
            elif await tools_handle(cmd, *args):
                pass
            elif cmd:
                await Console.error("\"%s\" command not found" % cmd.lower())


        except Exception as e:
            await Console.error(str(e) or repr(e))

    @staticmethod
    async def info(*messages):
        await aprint(Colorate.Diagonal(Colors.blue_to_white, "[!] " + ' '.join([txt for txt in messages])))
