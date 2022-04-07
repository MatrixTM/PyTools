from contextlib import suppress
from aioconsole import aprint
from asyncssh import SSHClientConnection, connect
from tools import Tool


class SSH(Tool):
    @staticmethod
    async def run(console, *args):
        assert len(args) == 2, "Usage: SSH <Ip:Port> <username>"
        ip, username = str(args[0]).split(":"), args[1]
        password = await console.cinput("Enter Password", hide_value=True)
        console.using.set()
        console.loading_text = f"Connecting To {ip[0]}"
        with suppress(KeyboardInterrupt):
            Connection: SSHClientConnection

            async with connect(ip[0], port=int(ip[1]), username=username, password=password,
                               known_hosts=None, connect_timeout=5) as Connection:
                await console.banner()
                while True:
                    inputcmd = await console.cinput(f"{username}@{ip[0]}")
                    output = await Connection.run(inputcmd)
                    await aprint(output.stdout)
