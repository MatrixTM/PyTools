from asyncio import run
from contextlib import suppress

from common import Console

if __name__ == '__main__':
    console = Console()
    run(console.banner())
    while 1:
        with suppress(KeyboardInterrupt):
            print()
            run(console.run())
