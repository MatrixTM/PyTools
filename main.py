from pystyle import Colorate, Colors, Center
from contextlib import suppress
from socket import gethostname
from os import system, name



def clear():
    system('cls' if name == 'nt' else 'clear')


def Header():
    clear()
    print(Colorate.Diagonal(Colors.yellow_to_red, Center.XCenter("""
                            ╔════════════════════════════════════════════════════════════════════════════════╗
                            ║    ooooooooo.              ooooooooooooo                     oooo              ║
                            ║    `888   `Y88.             8'   888   `8                     `888             ║
                            ║     888   .d88' oooo    ooo      888       .ooooo.   .ooooo.   888   .oooo.o   ║
                            ║     888ooo88P'   `88.  .8'       888      d88' `88b d88' `88b  888  d88(  "8   ║
                            ║     888           `88..8'        888      888   888 888   888  888  `"Y88b.    ║
                            ║     888            `888'         888      888   888 888   888  888  o.  )88b   ║
                            ║    o888o            .8'         o888o     `Y8bod8P' `Y8bod8P' o888o 8""888P'   ║
                            ║                 .o..P'                                                         ║
                            ║                 `Y8P'                                                          ║
                            ╚═══════════════════════╦═════════════════════════════════╦══════════════════════╝
                                                    ║   Coded By : SudoLite - V 1.0   ║
                                                    ╚═════════════════════════════════╝\n\n\n\n""")))


def inputstyle(text=None):
    return input(Colorate.Horizontal(Colors.yellow_to_red, f"╔═══[{gethostname()}{text}@PyTools]\n╚══════> "))



if __name__ == '__main__':
    Header()
    cons = f"╔═══[{gethostname()}@PyTools]\n╚══════ >"
    with suppress(KeyboardInterrupt):
        with suppress(IndexError):
            while 1:
                cmd = inputstyle("test").strip()
                if not cmd: continue
                if " " in cmd:
                    cmd, args = cmd.split(" ", 1)

                cmd = cmd.upper()
                if cmd == "HELP":
                    print("Commands: HELP, CLEAR, BACK, EXIT")
                    continue
