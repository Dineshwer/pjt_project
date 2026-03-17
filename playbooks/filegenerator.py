import yaml
import random
import string
from datetime import datetime, timedelta

OUTPUT = "../playbooks/filesystem.yaml"

USERS = ["admin", "ubuntu", "devops", "backup"]

COMMON_FILES = [
    "notes.txt",
    "todo.txt",
    "backup.sql",
    "passwords_old.txt",
    "vpn_config.ovpn",
]

LOG_TYPES = [
    "auth.log",
    "syslog",
    "kern.log",
]

def file_node(content):
    return {
        "type": "file",
        "content": content
    }

def dir_node(children=None):
    return {
        "type": "dir",
        "children": children if children else {}
    }

def random_ip():
    return f"{random.randint(10,200)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_logs():

    lines = []

    now = datetime.now()

    for _ in range(200):

        t = now - timedelta(minutes=random.randint(1,20000))

        ip = random_ip()

        lines.append(
            f"{t.strftime('%b %d %H:%M:%S')} svr04 sshd[{random.randint(1000,5000)}]: "
            f"Accepted password for admin from {ip} port {random.randint(2000,65000)} ssh2"
        )

    return "\n".join(lines)

def generate_passwd():

    return """root:x:0:0:root:/root:/bin/bash
admin:x:1000:1000:Admin:/home/admin:/bin/bash
ubuntu:x:1001:1001:Ubuntu:/home/ubuntu:/bin/bash
devops:x:1002:1002:DevOps:/home/devops:/bin/bash
backup:x:1003:1003:Backup:/home/backup:/bin/bash
mysql:x:104:108:MySQL Server:/nonexistent:/bin/false
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
"""

def bash_history():

    cmds = [
        "sudo apt update",
        "sudo apt install nginx",
        "docker ps",
        "docker-compose up -d",
        "mysql -u root -p",
        "vim config.php",
        "scp backup.sql backup@192.168.1.50:/backup",
        "git pull origin main",
        "systemctl restart nginx",
    ]

    history = []

    for _ in range(random.randint(20,50)):
        history.append(random.choice(cmds))

    return "\n".join(history)

def random_secret():

    key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))

    return f"""AWS_ACCESS_KEY=AKIA{random.randint(100000,999999)}
AWS_SECRET_KEY={key}
"""

def generate_users():

    users = {}

    for u in USERS:

        files = {}

        files[".bash_history"] = file_node(bash_history())

        files[".ssh"] = dir_node({
            "authorized_keys": file_node("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...")
        })

        for f in COMMON_FILES:
            files[f] = file_node("sample data")

        if u == "admin":
            files["aws_credentials.txt"] = file_node(random_secret())

        users[u] = dir_node(files)

    return users

def generate_logs_dir():

    logs = {}

    for log in LOG_TYPES:
        logs[log] = file_node(generate_logs())

    return dir_node(logs)

def generate_web_app():

    return dir_node({
        "html": dir_node({
            "index.php": file_node("<?php echo 'Welcome'; ?>"),
            "config.php": file_node("""
$db_host="localhost";
$db_user="admin";
$db_pass="admin123";
""")
        })
    })

def generate_tmp():

    tmp = {}

    for i in range(2000):
        tmp[f"tmp_{i}.dat"] = file_node("temp")

    return dir_node(tmp)

def generate_apps():

    apps = {}

    for i in range(30):

        apps[f"service_{i}"] = dir_node({
            "main.py": file_node("print('service running')"),
            "config.json": file_node("{ 'env':'prod', 'debug':false }")
        })

    return dir_node(apps)

def generate_filesystem():

    fs = {
        "/": dir_node({

            "etc": dir_node({
                "passwd": file_node(generate_passwd()),
                "hostname": file_node("svr04"),
                "hosts": file_node("127.0.0.1 localhost"),
                "resolv.conf": file_node("nameserver 8.8.8.8")
            }),

            "home": dir_node(generate_users()),

            "var": dir_node({
                "log": generate_logs_dir(),
                "www": generate_web_app()
            }),

            "opt": dir_node({
                "apps": generate_apps()
            }),

            "tmp": generate_tmp(),

            "root": dir_node({
                "notes.txt": file_node("""
TODO
- rotate db password
- check backups
""")
            })

        })
    }

    return fs

def main():

    fs = generate_filesystem()

    with open(OUTPUT, "w") as f:
        yaml.dump(fs, f, sort_keys=False)

    print("filesystem.yaml generated successfully")

if __name__ == "__main__":
    main()
