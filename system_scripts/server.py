#!/usr/bin/python3

import os
from configobj import ConfigObj
import subprocess
from bullet import Bullet

print("server - Mounting of RLI folders\n")

config = ConfigObj(os.environ["PYTHON_SYSTEM_SCRIPT_CONFIG"], stringify=False)
bullet_style = {
    k: config["BULLET"].as_int(k) if k != "bullet" else config["BULLET"]["bullet"]
    for k in config["BULLET"].keys()
}

USERS = ["hendrik.huyskens", "admin"]
TARGETS = {
    "//192.168.10.14/rl-institut": "/home/local/RL-INSTITUT/hendrik.huyskens/rl-institut"
}

cli = Bullet(prompt="Select target", choices=list(TARGETS.keys()), **bullet_style)
source = cli.launch()
destination = TARGETS[source]

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
