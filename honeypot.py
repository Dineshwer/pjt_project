import socket
import threading
import paramiko
import os
from commands import handle
from datetime import datetime

if not os.path.exists("keys"):
    os.mkdir("keys")

KEY_PATH = "keys/ssh_host_rsa_key"

if os.path.exists(KEY_PATH):
    HOST_KEY = paramiko.RSAKey(filename=KEY_PATH)
else:
    HOST_KEY = paramiko.RSAKey.generate(2048)
    HOST_KEY.write_private_key_file(KEY_PATH)


class Server(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_channel_shell_request(self, channel):
        return True


def client_handler(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = Server()
    transport.start_server(server=server)

    channel = transport.accept(20)
    if channel is None:
        return

    channel.send("Welcome to Ubuntu 20.04.6 LTS\n")

    state = {"cwd": "/"}

    while True:
        channel.send(f"root@svr04:{state['cwd']}# ")

        data = channel.recv(1024)
        if not data:
            break

        cmd = data.decode(errors="ignore").strip()

        if not cmd:
            continue

        if cmd in ["exit", "logout"]:
            channel.send("logout\n")
            break

        output = handle(cmd, state)

        if output:
            channel.send(output + "\n")

        with open("logs/sessions.log", "a") as f:
            f.write(f"{datetime.now()} {addr} CMD={cmd} CWD={state['cwd']}\n")

    channel.close()


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 2222))
sock.listen(100)

print("[+] Custom SSH Honeypot running on port 2222")

while True:
    client, addr = sock.accept()
    threading.Thread(
        target=client_handler,
        args=(client, addr),
        daemon=True
    ).start()
