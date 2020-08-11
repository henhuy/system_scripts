
import os
import subprocess
from configobj import ConfigObj
from bullet import Bullet

print('fssh - Fast SSH\n')

config = ConfigObj(os.environ["PYTHON_SYSTEM_SCRIPT_CONFIG"], stringify=False)
bullet_style = {
    k: config["BULLET"].as_int(k) if k != "bullet" else config["BULLET"]["bullet"]
    for k in config["BULLET"].keys()
}

ssh_options = config["FSSH"]["SSH"]
tunnels = config["FSSH"]["TUNNEL"]

cli = Bullet(prompt='Choose option:', choices=['ssh', 'tunnel'], **bullet_style)
option = cli.launch()
if option == 'ssh':
    lookup = ssh_options
    prompt = 'Where do you want to connect to?'
elif option == 'tunnel':
    lookup = tunnels
    prompt = 'Where do you want to dig tunnel to?'
else:
    raise KeyError('Unknown option')

cli = Bullet(prompt=prompt, choices=list(lookup.keys()), **bullet_style)
chosen = cli.launch()

route = lookup[chosen].as_list("route")

if option == 'ssh':
    call = ['ssh'] + route
else:
    call = ['ssh', '-fNL'] + route
subprocess.call(call)
