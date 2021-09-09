import json
from os import system
from os import path
import sys

if len(sys.argv) != 2:
    print "missing argument 1"
    sys.exit(1)

arg1 = sys.argv[1]

# default config
config = {
    "cssh_file_path": "~/.clusterssh/clusters"
}

# load config from config file
tssh_config_file = path.expanduser('~/.tssh.json')
if path.exists(tssh_config_file):
    with open(tssh_config_file) as json_data_file:
        data = json.load(json_data_file)
        for key in data:
            config[key] = data[key]

# load cssh configs
cssh_conf = {}
with open(path.expanduser(config['cssh_file_path']), 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            s = line.split(None, 1)
            cssh_conf[s[0]] = s[1]

# recursively get servers
def get_servers(key):
    cfg = cssh_conf[key].split(' ')
    servers = []
    for i in range(0, len(cfg)):
        if cfg[i] in cssh_conf:
            servers.extend(get_servers(cfg[i]))
        else:
            servers.append(cfg[i])
    return servers

# returns all the cluster names
def get_clusters():
    return ' '.join(cssh_conf.keys())

# autocompelete mode: return all the cluster names
if arg1 == '__autocomplete':
    print get_clusters()

# cluster name given: split the terminal and connect to the servers
elif arg1 in cssh_conf:
    cmds = []
    servers = get_servers(arg1)

    # make panes
    for i in range(0, len(servers) - 1):
        cmds.append('tmux split-window -h')
        cmds.append('tmux select-layout tiled')

    # make layout
    if len(servers) % 2 == 1:
        cmds.append('tmux select-layout even-vertical')
    else:
        cmds.append('tmux select-layout tiled')

    # create ssh commands
    for i in range(0, len(servers)):
        cmds.append('tmux send-keys -t ' + str(i) + ' \'/usr/bin/ssh ' + servers[i] + '\' \'C-m\'')

    # select first pane
    cmds.append('tmux select-pane -t 0')

    # set multi-cursor mode!
    cmds.append('tmux set-window-option synchronize-panes')

    # name window
    cmds.append('tmux rename-window ' + arg1)

    # and go!
    system('; '.join(cmds))

# what now?
else:
    print arg1 + " is not a known cluster. try one of " + get_clusters()
    sys.exit(1)
