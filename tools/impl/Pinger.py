import asyncio
from contextlib import suppress
from itertools import cycle
from time import time

import aioconsole
from aiohttp import ClientSession
from aioping import ping
from pystyle import Colorate, Colors
from yarl import URL

from tools import Tool

dots = cycle(["|", "/", "-", "\\"])


class Timer:
    _start: time
    _done: time

    def __enter__(self):
        self._start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._done = time()

    def __aenter__(self):
        self._start = time()
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self._done = time()

    def is_done(self):
        return self._done is None

    def currentMs(self):
        return round((time() - self._start) * 1000, 2)

    def result(self):
        return round((self._done - self._start) * 1000, 2)


class Pinger(Tool):
    using = False

    @staticmethod
    async def run(*args):
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
            Pinger.using = True
            asyncio.create_task(Pinger.amim(args[0].upper(), address, port))

            while 1:
                request = await method(address, port)
                if not request[1]: bad += 1

                counter += 1

                await asyncio.sleep(0.5)
                pings.append(request[0])

                await aioconsole.aprint(
                    Colorate.Horizontal(Colors.green_to_cyan if request[1] else Colors.red_to_purple,
                                        "[%s] Reply from %s%sstatus %s protocol %s time: %sms" % (
                                            counter,
                                            address,
                                            (f" port {port} " if method not in [Pinger.ICMP, Pinger.HTTP] else " "),
                                            Pinger.status(request, method),
                                            args[0].upper(),
                                            request[0])))
        Pinger.using = False

    @staticmethod
    async def ICMP(IP, PORT):
        with suppress(asyncio.TimeoutError):
            return round(await ping(IP, timeout=5) * 1000, 2), True
        return 5000, False

    @staticmethod
    async def HTTP(IP, PORT):
        with suppress(asyncio.TimeoutError), Timer() as timer:
            async with ClientSession(trust_env=True) as session, \
                    session.get(IP, timeout=5) as r:
                result = r.status
            return timer.currentMs(), result
        return timer.result(), 408

    @staticmethod
    async def TCP(IP, PORT):
        with suppress(asyncio.TimeoutError), Timer() as timer:
            fut = asyncio.open_connection(IP, PORT)
            await asyncio.wait_for(fut, timeout=5)
            return timer.currentMs(), True
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
    def select(TXT):
        if TXT == "TCP":
            return Pinger.TCP
        # elif TXT == "UDP":
        #     return Pinger.UDP
        elif TXT == "ICMP":
            return Pinger.ICMP
        elif TXT == "HTTP":
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

    @staticmethod
    async def amim(method, target, port):
        while Pinger.using:
            await aioconsole.aprint(
                "[%s] Pinging %s%susing %s protocol" %
                (next(dots),
                 target,
                 (f" port {port} " if method not in ["ICMP", "HTTP"] else " "),
                 method),
                end="\r")
            await asyncio.sleep(.05)
