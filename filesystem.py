import yaml

FS = yaml.safe_load(open("playbooks/filesystem.yaml"))

def resolve(path, cwd):
    if not path.startswith("/"):
        path = cwd.rstrip("/") + "/" + path
    parts = [p for p in path.split("/") if p]
    node = FS["/"]
    for p in parts:
        if node["type"] != "dir" or p not in node["children"]:
            return None
        node = node["children"][p]
    return node

def ls(path, cwd):
    node = resolve(path or cwd, cwd)
    if not node or node["type"] != "dir":
        return "ls: cannot access"
    return "  ".join(node["children"].keys())

def cat(path, cwd):
    node = resolve(path, cwd)
    if not node or node["type"] != "file":
        return "cat: file not found"
    return node["content"]

def cd(path, cwd):

    # handle cd ..
    if path == "..":
        if cwd == "/":
            return "/"

        parts = cwd.strip("/").split("/")
        parts = parts[:-1]

        if not parts:
            return "/"

        return "/" + "/".join(parts)

    # handle cd .
    if path == ".":
        return cwd

    node = resolve(path, cwd)

    if not node or node["type"] != "dir":
        return cwd

    if not path.startswith("/"):
        if cwd == "/":
            return "/" + path
        return cwd.rstrip("/") + "/" + path

    return path

def pwd(cwd):
    return cwd
