from tools.impl.Pinger import Pinger
from tools.impl.cfxFinder import Cfxfinder
from tools.impl.SSH import SSH

__all__ = ["handle"]


async def handle(cmd, *args):
    if {cmd} & {"PING", "PINGER"}:
        await Pinger.run(*args)
        return True
    elif {cmd} & {"CFX"}:
        await Cfxfinder.run(*args)
        return True
    elif {cmd} & {"SSH"}:
        await SSH.run(*args)
        return True
    return False
