from asyncio import run
from contextlib import suppress

from common import Console

if __name__ == '__main__':
    run(Console.banner())
    while 1:
        with suppress(KeyboardInterrupt):
            print()
            run(Console.run())
