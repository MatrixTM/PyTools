from contextlib import suppress
from getpass import getpass
from aioconsole import aprint
from asyncssh import SSHClientConnection, connect
from tools import Tool


class SSH(Tool):
    using = False

    @staticmethod
    async def run(*args):
        assert len(args) == 2, "bad args"
        ip, username = str(args[0]).split(":"), args[1]  # SSH 185.855.855.690:22 root
        password = getpass("Enter Password: ")
        await aprint(f"Connecting To {ip[0]}")
        try:
            with suppress(KeyboardInterrupt):
                SSH.using = True
                try:
                    Connection: SSHClientConnection

                    async with connect(ip[0], port=int(ip[1]), username=username, password=password,
                                       known_hosts=None, connect_timeout=5) as Connection:
                        while True:
                            inputcmd = input(f"{username}@{ip[0]}> ")
                            output = await Connection.run(inputcmd)
                            await aprint(output.stdout)
                except Exception as e:
                    await aprint(str(e))
        finally:
            SSH.using = False
