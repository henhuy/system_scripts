
import os
import subprocess

import typer
from bullet import Bullet
from configobj import ConfigObj

LAPTOP_RESOLUTION = '1200x800'
DESKTOP_RESOLUTION = '1800x1000'

DEFAULT_USER = 'admin'

config = ConfigObj(os.environ['PYTHON_SYSTEM_SCRIPT_CONFIG'], stringify=False)
bullet_style = {
    k: config['BULLET'].as_int(
        k,
    ) if k != 'bullet' else config['BULLET']['bullet']
    for k in config['BULLET'].keys()
}

app = typer.Typer()
typer.echo('remote - Simple tool to connect to remote devices\n')


remotes = config["REMOTE"]


@app.command()
def remote(name: str = typer.Argument(None), laptop: bool = typer.Option(False, '-l')):
    if not name:
        cli = Bullet(prompt='Choose option:', choices=list(remotes.keys()), **bullet_style)
        name = cli.launch()
    typer.echo(f"Starting remote connection to '{name}'")

    if laptop:
        resolution = LAPTOP_RESOLUTION
        typer.echo('Using laptop resolution')
    else:
        resolution = DESKTOP_RESOLUTION

    try:
        address = remotes[name]
    except KeyError:
        typer.echo(f"Address '{name}' not found in remote addresses. Trying to use '{name}' as host address...")
        host = name
        user = DEFAULT_USER
        domain = None
    else:
        host = address['host']
        user = address['user']
        domain = address.get("domain")

    call = [
        'xfreerdp',
        f'/v:{host}',
        f'/u:{user}',
        f'/size:{resolution}',
    ]
    if domain:
        call += [f'/d:{domain}']
    typer.echo(f"Running: {' '.join(call)}")
    subprocess.call(call)


def main():
    app()


if __name__ == "__main__":
    main()
