
Daily bash scripts implemented in python

# Getting started

In order to run system scripts you can install them easily via pipx.
```bash
pipx install .
```
System scripts are looking for a config file. Therefore, the env variable `PYTHON_SYSTEM_SCRIPT_CONFIG` must be set.
The easiest way to permanently add it to the system, is by adding it to the `.profile` file in your home directory:
```bash
export PYTHON_SYSTEM_SCRIPT_CONFIG=<path to config file>
```

Following commands are available:

fssh - Connects to config-defined servers via ssh (or creates defined tunnels)
remote - Connects to remote servers (defined in config) via xfreerdp
server - Mounts/unmounts servers (config file) via mount.cifs
redmine - Crawls Redmine for specific user information

Config file is read via ConfigParser and must look like:

```
[REMOTE]
    [[Servername]]
	host = <hostip>
	user = <username>
    [[Servername2]]
	host = <hostip>
	user = <username>

[FSSH]
    [[SSH]]
        [[[name]]]
            route = <username@server>
        [[[name2]]]
            route = <username@server>
    [[TUNNEL]]
        [[[tunnelname]]]
            route = <port_local:localhost:port_remote, username@server>

[SERVER]
    [[name]]
        source = <//server_ip/remote_folder>
        destination = <local_folder>
```