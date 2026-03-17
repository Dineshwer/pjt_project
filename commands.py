import yaml
from filesystem import ls, cat, cd, pwd

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
