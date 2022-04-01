import asyncio
from os import name
from socket import gethostname

from aioconsole import aprint, ainput
from pystyle import Colorate, Colors, Center


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
    async def clear():
        await Console.command('cls' if name == 'nt' else 'clear')

    @staticmethod
    async def run():
        await Console.banner()
        while 1:
            inp = (await Console.input(Colorate.Horizontal(Colors.yellow_to_red,
                                                           f"╔═══[{gethostname()}"
                                                           f"@PyTools]\n╚══════> "))).strip()
            if not inp: pass
            await Console.handle(inp)

    @staticmethod
    async def command(cmds):
        return (await asyncio.create_subprocess_shell(*cmds.split(" "))).communicate()

    @staticmethod
    async def handle(inp):
        cmd, args = (inp + " ").split(" ", 1)
        cmd = cmd.upper()
        args = args or []

        if {cmd} & {"HELP", "?"}:
            await aprint("help ?")


if __name__ == '__main__':
    asyncio.run(Console.run())
