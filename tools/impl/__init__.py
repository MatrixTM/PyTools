from tools.impl.Pinger import Pinger


__all__ = ["handle"]

async def handle(cmd, *args):
    if {cmd} & {"PING", "PINGER"}:
        await Pinger.run(*args)
        return True
    return False
