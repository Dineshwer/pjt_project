import yaml
from filesystem import ls, cat, cd, pwd, touch, mkdir, rm

PLAYBOOK = yaml.safe_load(open("playbooks/commands.yaml"))

def handle(cmdline, state):

    args = cmdline.split()

    if not args:
        return ""

    cmd = args[0]

    # -------------------------
    # filesystem commands
    # -------------------------

    if cmd == "ls":
        path = args[1] if len(args) > 1 else ""
        return ls(path, state["cwd"])
    # -------------------------
    # write filesystem commands
    # -------------------------

    if cmd == "touch":
        if len(args) < 2:
            return "touch: missing file"
        return touch(args[1], state["cwd"])

    if cmd == "mkdir":
        if len(args) < 2:
            return "mkdir: missing directory"
        return mkdir(args[1], state["cwd"])

    if cmd == "rm":
        if len(args) < 2:
            return "rm: missing file"
        return rm(args[1], state["cwd"])

    if cmd == "cat":
        if len(args) < 2:
            return "cat: missing file"
        return cat(args[1], state["cwd"])

    if cmd == "cd":

        if len(args) == 1:
            state["cwd"] = "/"
        else:
            state["cwd"] = cd(args[1], state["cwd"])

        return ""

    if cmd == "pwd":
        return pwd(state["cwd"])

    # -------------------------
    # playbook commands
    # -------------------------

    # exact command (example: uname -a)
    if cmdline in PLAYBOOK["commands"]:
        return PLAYBOOK["commands"][cmdline]

    # base command (example: uname)
    if cmd in PLAYBOOK["commands"]:
        return PLAYBOOK["commands"][cmd]

    return f"{cmdline}: command not found"
