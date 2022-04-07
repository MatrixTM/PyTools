from tools.impl.Pinger import Pinger
from tools.impl.cfxFinder import Cfxfinder
from tools.impl.SSH import SSH

__all__ = ["handle"]


async def handle(console, cmd, *args):
    if {cmd} & {"PING", "PINGER"}:
        await Pinger.run(console, *args)
        return True
    elif {cmd} & {"CFX"}:
        await Cfxfinder.run(console, *args)
        return True
    elif {cmd} & {"SSH"}:
        await SSH.run(console, *args)
        return True
    return False
