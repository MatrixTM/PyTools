from asyncio import sleep, open_connection, TimeoutError, wait_for
from contextlib import suppress

from aioconsole import aprint
from aiohttp import ClientSession
from aioping import ping
from pystyle import Colorate, Colors
from yarl import URL

from tools import Tool, Timer


# noinspection PyUnusedLocal
class Pinger(Tool):
    @staticmethod
    async def run(console, *args):
        assert len(args) == 2, "bad args"

        bad = 0
        counter = 0
        pings = []

        target = URL(args[1] if args[1].startswith("http") else ("http://" + args[1]))
        method = Pinger.select(args[0].upper())

        port = target.port or 80

        assert method, "invalid method"

        address = target.human_repr() if method == Pinger.HTTP else target.host
        with suppress(KeyboardInterrupt):
            console.using.set()
            console.loading_text = "Pinging %s%susing %s protocol" % (address,
                                                                      (f" port {port} " if args[0].upper() not in [
                                                                          "ICMP", "HTTP"] else " "),
                                                                      args[0].upper())

            while 1:
                request = await method(address, port)
                if not request[1] and request[1] != 408:
                    bad += 1

                counter += 1

                await sleep(0.5)
                pings.append(request[0])

                await aprint(
                    Colorate.Horizontal(
                        Colors.green_to_cyan if request[1] and request[1] != 408 else Colors.red_to_purple,
                        "[%s] Reply from %s%sstatus %s protocol %s time: %sms" % (
                            counter,
                            address,
                            (f" port {port} " if method not in [Pinger.ICMP, Pinger.HTTP] else " "),
                            Pinger.status(request, method),
                            args[0].upper(),
                            request[0])))

    @staticmethod
    async def ICMP(ip, port):
        with suppress(TimeoutError):
            return round(await ping(ip, timeout=5) * 1000, 2), True
        return 5000, False

    @staticmethod
    async def HTTP(ip, port):
        with suppress(TimeoutError), Timer() as timer:
            async with ClientSession(trust_env=True) as session, \
                    session.get(ip, timeout=5) as r:
                result = r.status
            return timer.currentms(), result
        return timer.result(), 408

    @staticmethod
    async def TCP(ip, port):
        with suppress(TimeoutError), Timer() as timer:
            await wait_for(open_connection(ip, port), timeout=5)
            return timer.currentms(), True
        return timer.result(), False

    # @staticmethod
    # async def UDP(IP, PORT):
    #     with suppress(asyncio.TimeoutError), Timer() as timer:
    #         with asyncoro.AsynCoroSocket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
    #             await sock.sendto(b'\0x00', (IP, PORT))
    #             await sock.recvfrom(1)
    #         return timer.currentMs(), True
    #     return timer.currentMs(), False

    @staticmethod
    def select(txt):
        if txt == "TCP":
            return Pinger.TCP
        # elif TXT == "UDP":
        #     return Pinger.UDP
        elif txt == "ICMP":
            return Pinger.ICMP
        elif txt == "HTTP":
            return Pinger.HTTP
        else:
            return None

    @staticmethod
    def status(request, method):
        if method is Pinger.HTTP:
            s = str(request[1])
        # elif method is Pinger.UDP:
        #     s = "LOAD OR FILTER"
        elif request[1]:
            s = "LOAD"
        else:
            s = "OVERLOAD"
        return s
