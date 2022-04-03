from tools.impl.Pinger import Pinger
from tools.impl.cfxFinder import cfxFinder


__all__ = ["handle"]

async def handle(cmd, *args):
    if {cmd} & {"PING", "PINGER"}:
        await Pinger.run(*args)
        return True
    elif {cmd} & {"CFX"}:
        await cfxFinder.run(*args)
        return True
    return False
