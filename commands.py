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

    # =====================================================
    # 🔥 NEW ATTACK SIMULATION COMMANDS (ADDED HERE)
    # =====================================================

    import time
    import re

    # -------------------------
    # CURL / WGET (Download)
    # -------------------------
    if cmd.startswith("curl") or cmd.startswith("wget"):
        time.sleep(1)

        url_match = re.search(r'(https?://\S+)', cmdline)
        url = url_match.group(0) if url_match else "unknown"

        filename = url.split("/")[-1] if url != "unknown" else "file.sh"

        # ✅ CREATE FILE (FIX)
        touch(filename, state["cwd"])

        return f"Downloading {filename}...\nSaved as {filename}"

    # -------------------------
    # CHMOD
    # -------------------------
    if cmd == "chmod":
        return ""

    # -------------------------
    # SCRIPT EXECUTION
    # -------------------------
    if cmd.startswith("./"):
        time.sleep(1)
        return (
            "[*] Executing script...\n"
            "[*] Collecting /var data...\n"
            "[*] Collecting /etc data...\n"
            "[*] Collecting /home data...\n"
            "[*] Compressing data...\n"
            "[*] Exfiltrating data to remote server...\n"
            "[*] Operation completed."
        )

    # -------------------------
    # TAR (compression)
    # -------------------------
    if cmd == "tar":
        time.sleep(1)
        return "Archive created successfully."

    # -------------------------
    # EXFILTRATION (curl POST)
    # -------------------------
    if "curl -X POST" in cmdline:
        time.sleep(1)
        return "Uploading data to remote server..."

    # -------------------------
    # NETCAT
    # -------------------------
    if cmd == "nc":
        return "Connection established."

    # -------------------------
    # ECHO
    # -------------------------
    if cmd == "echo":
        return cmdline.replace("echo ", "")

    # -------------------------
    # HISTORY CLEAR
    # -------------------------
    if cmd.startswith("history"):
        return ""

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
