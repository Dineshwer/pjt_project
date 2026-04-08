import time
import os

LOG_FILE = "sessions.log"
ALERT_FILE = "alerts.log"

# Keywords to watch
ALERT_KEYWORDS = {"curl", "wget", "chmod", "bash", "netstat", "rm"}


def follow(file):
    """Generator that yields new lines (like tail -f)"""
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line.strip()


def extract_cmd(log_line):
    """Extract command from log line"""
    try:
        cmd_part = log_line.split("CMD=")[1]
        cmd = cmd_part.split()[0]
        return cmd.lower()
    except IndexError:
        return None


def alert(line, cmd):
    """Handle alert (print + write to file)"""
    alert_message = (
        f"🚨 ALERT! Suspicious command detected!\n"
        f"Command: {cmd}\n"
        f"Log: {line}\n"
        f"{'-'*50}\n"
    )

    # Print to console
    print(alert_message)

    # Write to alerts.log
    with open(ALERT_FILE, "a") as f:
        f.write(alert_message)


def monitor():
    if not os.path.exists(LOG_FILE):
        print(f"Log file '{LOG_FILE}' not found.")
        return

    # Ensure alert file exists
    open(ALERT_FILE, "a").close()

    with open(LOG_FILE, "r") as f:
        loglines = follow(f)

        for line in loglines:
            cmd = extract_cmd(line)
            if cmd:
                for keyword in ALERT_KEYWORDS:
                    if keyword in cmd:
                        alert(line, cmd)
                        break


if __name__ == "__main__":
    print("🔍 Monitoring sessions.log...")
    monitor()
