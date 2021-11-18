import os
import subprocess

import typer
from bullet import Bullet
from configobj import ConfigObj

app = typer.Typer()
typer.echo("server - Mounting of RLI folders\n")

config = ConfigObj(os.environ["PYTHON_SYSTEM_SCRIPT_CONFIG"], stringify=False)
bullet_style = {
    k: config["BULLET"].as_int(k) if k != "bullet" else config["BULLET"]["bullet"]
    for k in config["BULLET"].keys()
}

USERS = ["hendrik.huyskens", "admin"]
TARGETS = config["SERVER"]


@app.command()
def server():
    cli = Bullet(prompt="Select target", choices=list(TARGETS.keys()), **bullet_style)
    target = cli.launch()
    source = TARGETS[target]["source"]
    destination = TARGETS[target]["destination"]

    if os.path.ismount(destination):
        cli = Bullet(
            prompt="Already mounted - do you want to unmount it?",
            choices=["yes", "no"],
            **bullet_style,
        )
        if cli.launch() == "yes":
            subprocess.call(["sudo", "umount", "-f", destination])
        exit()

    cli = Bullet(prompt="Choose user:", choices=USERS, **bullet_style)
    user = cli.launch()

    cmd = [
        "sudo",
        "mount.cifs",
        "-o",
        f"user={user},dom=rl-institut,uid=RL-INSTITUT\\hendrik.huyskens",
        source,
        destination,
    ]
    subprocess.call(cmd)


def main():
    app()
