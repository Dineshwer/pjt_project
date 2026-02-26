import yaml
from filesystem import ls, cat, cd, pwd

PLAYBOOK = yaml.safe_load(open("playbooks/commands.yaml"))

def handle(cmd, state):
    args = cmd.split()

    if args[0] == "ls":
        return ls(args[1] if len(args) > 1 else "", state["cwd"])

    if args[0] == "cat" and len(args) > 1:
        return cat(args[1], state["cwd"])

    if args[0] == "cd" and len(args) > 1:
        state["cwd"] = cd(args[1], state["cwd"])
        return ""

    if args[0] == "pwd":
        return pwd(state["cwd"])

    return PLAYBOOK["commands"].get(cmd, f"{cmd}: command not found")
