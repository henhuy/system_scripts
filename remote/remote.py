
import subprocess
from dataclasses import dataclass
from typing import Dict, Optional

import typer
from bullet import Bullet

LAPTOP_RESOLUTION = "1200x800"
DESKTOP_RESOLUTION = "1800x1000"

app = typer.Typer()


@dataclass
class RemoteAddress:
    ip: str
    user: str = "hendrik.huyskens"
    domain: Optional[str] = "rl-institut"


ADDRESSES: Dict[str, RemoteAddress] = {
    "DC1": RemoteAddress("192.168.10.200", "admin"),
    "SRVEX": RemoteAddress("192.168.10.8", "admin"),
}


@app.command()
def remote(name: str = typer.Argument(None), laptop: bool = typer.Option(False, "-l")):
    if not name:
        cli = Bullet(prompt="Choose option:", choices=list(ADDRESSES.keys()))
        name = cli.launch()
    typer.echo(f"Starting remote connection to '{name}'")

    if laptop:
        resolution = LAPTOP_RESOLUTION
        typer.echo("Using laptop resolution")
    else:
        resolution = DESKTOP_RESOLUTION

    address = ADDRESSES[name]

    call = [
        "rdesktop",
        address.ip,
        "-u",
        address.user,
        "-g",
        resolution,
    ]
    if address.domain:
        call += ["-d", address.domain]
    subprocess.call(call)


def main():
    app()
