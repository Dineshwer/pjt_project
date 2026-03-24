import yaml
import random
import string
from datetime import datetime, timedelta

OUTPUT = "filesystem.yaml"

# ─────────────────────────────────────────────
# ENTERPRISE USER ROSTER
# ─────────────────────────────────────────────
USERS = [
    "admin", "ubuntu", "devops", "backup", "jenkins", "deploy",
    "dbadmin", "sysadmin", "netadmin", "monitor", "ansible",
    "terraform", "k8sadmin", "secops", "auditor", "readonly",
    "appuser", "dataeng", "mlops", "financeadmin"
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def file_node(content):
    return {"type": "file", "content": str(content)}

def dir_node(children=None):
    return {"type": "dir", "children": children if children else {}}

def random_ip(private=False):
    if private:
        return f"10.{random.randint(0,10)}.{random.randint(1,50)}.{random.randint(1,254)}"
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def rand_str(n=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def rand_hex(n=40):
    return ''.join(random.choices('0123456789abcdef', k=n))

def rand_port():
    return random.randint(30000, 65000)

def timestamp(offset_mins=None):
    if offset_mins is None:
        offset_mins = random.randint(1, 525600)
    t = datetime.now() - timedelta(minutes=offset_mins)
    return t.strftime('%Y-%m-%d %H:%M:%S')

# ─────────────────────────────────────────────
# /etc
# ─────────────────────────────────────────────
def generate_passwd():
    entries = [
        "root:x:0:0:root:/root:/bin/bash",
        "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin",
        "bin:x:2:2:bin:/bin:/usr/sbin/nologin",
        "sys:x:3:3:sys:/dev:/usr/sbin/nologin",
        "sync:x:4:65534:sync:/bin:/bin/sync",
        "games:x:5:60:games:/usr/games:/usr/sbin/nologin",
        "man:x:6:12:man:/var/cache/man:/usr/sbin/nologin",
        "lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin",
        "mail:x:8:8:mail:/var/mail:/usr/sbin/nologin",
        "news:x:9:9:news:/var/spool/news:/usr/sbin/nologin",
        "uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin",
        "proxy:x:13:13:proxy:/bin:/usr/sbin/nologin",
        "www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin",
        "backup:x:34:34:backup:/var/backups:/usr/sbin/nologin",
        "list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin",
        "nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin",
        "systemd-network:x:100:102:systemd Network Management:/run/systemd:/usr/sbin/nologin",
        "systemd-resolve:x:101:103:systemd Resolver:/run/systemd:/usr/sbin/nologin",
        "syslog:x:102:106::/home/syslog:/usr/sbin/nologin",
        "messagebus:x:103:107::/nonexistent:/usr/sbin/nologin",
        "sshd:x:104:65534::/run/sshd:/usr/sbin/nologin",
        "pollinate:x:105:1::/var/cache/pollinate:/bin/false",
        "usbmux:x:106:46:usbmux daemon:/var/lib/usbmux:/usr/sbin/nologin",
        "mysql:x:107:115:MySQL Server:/nonexistent:/bin/false",
        "redis:x:108:116::/var/lib/redis:/usr/sbin/nologin",
        "postgres:x:109:117:PostgreSQL administrator:/var/lib/postgresql:/bin/bash",
        "nginx:x:110:118:nginx user:/nonexistent:/usr/sbin/nologin",
        "prometheus:x:111:119::/var/lib/prometheus:/usr/sbin/nologin",
        "grafana:x:112:120::/usr/share/grafana:/bin/false",
        "elasticsearch:x:113:121::/usr/share/elasticsearch:/bin/false",
        "vault:x:114:122:HashiCorp Vault:/var/lib/vault:/usr/sbin/nologin",
        "consul:x:115:123:HashiCorp Consul:/var/lib/consul:/usr/sbin/nologin",
    ]
    uid = 1000
    for u in USERS:
        entries.append(f"{u}:x:{uid}:{uid}:{u.capitalize()} User:/home/{u}:/bin/bash")
        uid += 1
    return "\n".join(entries) + "\n"

def generate_shadow():
    lines = ["root:$6$" + rand_str(8) + "$" + rand_str(86) + ":19000:0:99999:7:::"]
    for u in USERS:
        lines.append(f"{u}:$6${rand_str(8)}${rand_str(86)}:19200:0:99999:7:::")
    return "\n".join(lines) + "\n"

def generate_group():
    lines = [
        "root:x:0:", "daemon:x:1:", "bin:x:2:", "sys:x:3:", "adm:x:4:syslog,admin",
        "tty:x:5:", "disk:x:6:", "lp:x:7:", "mail:x:8:", "news:x:9:",
        "uucp:x:10:", "man:x:12:", "proxy:x:13:", "kmem:x:15:", "dialout:x:20:",
        "fax:x:21:", "voice:x:22:", "cdrom:x:24:", "floppy:x:25:", "tape:x:26:",
        "sudo:x:27:admin,devops,sysadmin", "audio:x:29:", "dip:x:30:", "www-data:x:33:",
        "backup:x:34:", "operator:x:37:", "list:x:38:", "irc:x:39:", "src:x:40:",
        "gnats:x:41:", "shadow:x:42:", "utmp:x:43:", "video:x:44:", "sasl:x:45:",
        "plugdev:x:46:", "staff:x:50:", "games:x:60:", "users:x:100:",
        "nobody:x:65534:", "docker:x:999:admin,devops,jenkins,deploy",
        "ssl-cert:x:998:", "mysql:x:115:", "redis:x:116:", "postgres:x:117:",
        "devteam:x:2000:devops,appuser,dataeng,mlops",
        "infra:x:2001:devops,sysadmin,netadmin,ansible,terraform",
        "security:x:2002:secops,auditor,sysadmin",
    ]
    uid = 1000
    for u in USERS:
        lines.append(f"{u}:x:{uid}:")
        uid += 1
    return "\n".join(lines) + "\n"

def generate_sudoers():
    return """# This file MUST be edited with the 'visudo' command as root.
Defaults	env_reset
Defaults	mail_badpass
Defaults	secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults	logfile=/var/log/sudo.log
Defaults	log_input,log_output

root	ALL=(ALL:ALL) ALL
%admin	ALL=(ALL) ALL
%sudo	ALL=(ALL:ALL) ALL

# Infrastructure team
devops	ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/local/bin/kubectl, /bin/systemctl
sysadmin ALL=(ALL) NOPASSWD: ALL
ansible ALL=(ALL) NOPASSWD: ALL
terraform ALL=(root) NOPASSWD: /usr/local/bin/terraform
jenkins ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/local/bin/kubectl
deploy  ALL=(ALL) NOPASSWD: /usr/bin/docker, /bin/systemctl restart *, /usr/bin/rsync
netadmin ALL=(root) NOPASSWD: /sbin/iptables, /sbin/ip, /usr/sbin/tcpdump
k8sadmin ALL=(ALL) NOPASSWD: /usr/local/bin/kubectl, /usr/local/bin/helm
dbadmin ALL=(postgres) NOPASSWD: /usr/bin/psql, ALL
"""

def generate_sshd_config():
    return """# SSH Server Configuration - CORP-INFRA-SVR04
Port 22
AddressFamily inet
ListenAddress 0.0.0.0

HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

SyslogFacility AUTH
LogLevel INFO

LoginGraceTime 2m
PermitRootLogin prohibit-password
StrictModes yes
MaxAuthTries 6
MaxSessions 10

PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

PasswordAuthentication yes
PermitEmptyPasswords no
ChallengeResponseAuthentication no

UsePAM yes
X11Forwarding no
PrintMotd no

ClientAliveInterval 300
ClientAliveCountMax 2

AllowGroups sudo devteam infra security

Banner /etc/ssh/banner.txt
"""

def generate_crontab():
    return """# /etc/crontab: system-wide crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )

# Database backups
0 2 * * *  dbadmin  /opt/scripts/db_backup.sh >> /var/log/db_backup.log 2>&1
30 2 * * * backup   /opt/scripts/s3_sync.sh >> /var/log/s3_sync.log 2>&1

# Health checks
*/5 * * * * monitor /opt/scripts/health_check.sh > /dev/null 2>&1

# Certificate renewal
0 3 * * 1  root     certbot renew --quiet >> /var/log/certbot.log 2>&1

# Log rotation
0 0 * * *  root     /usr/sbin/logrotate /etc/logrotate.conf

# Prometheus node exporter metrics flush
*/1 * * * * prometheus /opt/prometheus/flush_metrics.sh > /dev/null 2>&1

# Security audit
0 4 * * *  secops   /opt/scripts/audit_scan.sh >> /var/log/security_audit.log 2>&1
"""

def generate_hosts():
    lines = [
        "127.0.0.1 localhost",
        "127.0.1.1 svr04.corp.internal svr04",
        "",
        "# Kubernetes cluster nodes",
        "10.0.1.10 k8s-master-01.corp.internal k8s-master-01",
        "10.0.1.11 k8s-master-02.corp.internal k8s-master-02",
        "10.0.1.12 k8s-master-03.corp.internal k8s-master-03",
        "10.0.1.20 k8s-worker-01.corp.internal k8s-worker-01",
        "10.0.1.21 k8s-worker-02.corp.internal k8s-worker-02",
        "10.0.1.22 k8s-worker-03.corp.internal k8s-worker-03",
        "10.0.1.23 k8s-worker-04.corp.internal k8s-worker-04",
        "10.0.1.24 k8s-worker-05.corp.internal k8s-worker-05",
        "",
        "# Database cluster",
        "10.0.2.10 db-primary.corp.internal db-primary",
        "10.0.2.11 db-replica-01.corp.internal db-replica-01",
        "10.0.2.12 db-replica-02.corp.internal db-replica-02",
        "10.0.2.20 redis-master.corp.internal redis-master",
        "10.0.2.21 redis-replica.corp.internal redis-replica",
        "",
        "# Infrastructure services",
        "10.0.3.10 jenkins.corp.internal jenkins",
        "10.0.3.11 gitlab.corp.internal gitlab",
        "10.0.3.12 nexus.corp.internal nexus",
        "10.0.3.13 sonarqube.corp.internal sonarqube",
        "10.0.3.14 vault.corp.internal vault",
        "10.0.3.15 consul.corp.internal consul",
        "10.0.3.16 prometheus.corp.internal prometheus",
        "10.0.3.17 grafana.corp.internal grafana",
        "10.0.3.18 kibana.corp.internal kibana",
        "10.0.3.19 elasticsearch.corp.internal elasticsearch",
        "",
        "# Load balancers",
        "10.0.4.10 lb-01.corp.internal lb-01",
        "10.0.4.11 lb-02.corp.internal lb-02",
        "10.0.4.12 lb-03.corp.internal lb-03",
        "",
        "# Storage",
        "10.0.5.10 nas-01.corp.internal nas-01",
        "10.0.5.11 nfs-01.corp.internal nfs-01",
        "10.0.5.12 s3-gateway.corp.internal s3-gateway",
        "",
        "::1 ip6-localhost ip6-loopback",
        "fe00::0 ip6-localnet",
        "ff00::0 ip6-mcastprefix",
    ]
    return "\n".join(lines)

def generate_resolv():
    return """# Generated by NetworkManager
search corp.internal aws.internal
nameserver 10.0.0.2
nameserver 10.0.0.3
nameserver 8.8.8.8
options ndots:5 timeout:2 attempts:3
"""

def generate_environment():
    return """PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
GOPATH="/home/devops/go"
KUBECONFIG="/home/k8sadmin/.kube/config"
VAULT_ADDR="https://vault.corp.internal:8200"
CONSUL_HTTP_ADDR="https://consul.corp.internal:8500"
DOCKER_HOST="unix:///var/run/docker.sock"
TF_LOG="WARN"
"""

def generate_iptables():
    return """# Generated by iptables-save
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]

# Allow established connections
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow loopback
-A INPUT -i lo -j ACCEPT

# Allow SSH
-A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
-A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 5 -j DROP
-A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT

# Allow internal k8s cluster
-A INPUT -s 10.0.1.0/24 -j ACCEPT

# Allow monitoring
-A INPUT -p tcp --dport 9090 -s 10.0.3.16 -j ACCEPT
-A INPUT -p tcp --dport 9100 -s 10.0.3.16 -j ACCEPT

# Allow internal comms
-A INPUT -s 10.0.0.0/8 -j ACCEPT

# Drop everything else
-A INPUT -j LOG --log-prefix "IPTABLES-DROP: " --log-level 7
-A INPUT -j DROP

COMMIT
"""

def generate_nginx_conf():
    return """user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    gzip  on;
    gzip_types text/plain application/json application/javascript text/css;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
"""

def generate_mysql_conf():
    return """[mysqld]
user            = mysql
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
port            = 3306
basedir         = /usr
datadir         = /var/lib/mysql
tmpdir          = /tmp
lc-messages-dir = /usr/share/mysql
bind-address    = 10.0.2.10

# Performance
innodb_buffer_pool_size = 4G
innodb_buffer_pool_instances = 4
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
max_connections = 500
thread_cache_size = 16
table_open_cache = 4000
query_cache_size = 256M
query_cache_type = 1

# Replication
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = appdb
binlog_do_db = userdb
binlog_do_db = analyticsdb
expire_logs_days = 10
max_binlog_size = 100M

[mysqldump]
quick
quote-names
max_allowed_packet = 64M
"""

def generate_etc():
    return dir_node({
        "passwd": file_node(generate_passwd()),
        "shadow": file_node(generate_shadow()),
        "group": file_node(generate_group()),
        "sudoers": file_node(generate_sudoers()),
        "hostname": file_node("svr04.corp.internal"),
        "hosts": file_node(generate_hosts()),
        "resolv.conf": file_node(generate_resolv()),
        "environment": file_node(generate_environment()),
        "timezone": file_node("America/New_York"),
        "issue": file_node("Ubuntu 22.04.3 LTS \\n \\l"),
        "issue.net": file_node("Ubuntu 22.04.3 LTS"),
        "os-release": file_node("NAME=\"Ubuntu\"\nVERSION=\"22.04.3 LTS (Jammy Jellyfish)\"\nID=ubuntu\nID_LIKE=debian\nPRETTY_NAME=\"Ubuntu 22.04.3 LTS\"\nVERSION_ID=\"22.04\"\nHOME_URL=\"https://www.ubuntu.com/\"\nSUPPORT_URL=\"https://help.ubuntu.com/\""),
        "fstab": file_node("UUID=a6c6-b4f2 /               ext4 errors=remount-ro 0 1\nUUID=b71a-9e43 /boot/efi       vfat umask=0077 0 1\nUUID=d8f2-3310 /data           ext4 defaults 0 2\n/dev/mapper/swap none swap sw 0 0\n10.0.5.10:/exports/shared /mnt/nfs nfs defaults 0 0"),
        "crontab": file_node(generate_crontab()),
        "iptables": dir_node({"rules.v4": file_node(generate_iptables())}),
        "ssh": dir_node({
            "sshd_config": file_node(generate_sshd_config()),
            "banner.txt": file_node("\n*** AUTHORIZED ACCESS ONLY ***\nThis system is property of CORP. All activity is monitored and logged.\nUnauthorized access is prohibited and will be prosecuted to the full extent of the law.\n"),
            "ssh_host_rsa_key.pub": file_node("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... root@svr04"),
            "ssh_host_ed25519_key.pub": file_node("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH... root@svr04"),
        }),
        "nginx": dir_node({
            "nginx.conf": file_node(generate_nginx_conf()),
            "mime.types": file_node("types { text/html html htm shtml; text/css css; text/xml xml; application/json json; application/javascript js; }"),
            "conf.d": dir_node({
                "default.conf": file_node("server { listen 80; server_name _; return 301 https://$host$request_uri; }"),
                "api.conf": file_node("upstream api_backend { server 10.0.1.20:8080; server 10.0.1.21:8080; server 10.0.1.22:8080; }\nserver { listen 443 ssl; server_name api.corp.internal; ssl_certificate /etc/letsencrypt/live/api.corp.internal/fullchain.pem; ssl_certificate_key /etc/letsencrypt/live/api.corp.internal/privkey.pem; location / { proxy_pass http://api_backend; proxy_set_header Host $host; } }"),
                "grafana.conf": file_node("server { listen 443 ssl; server_name grafana.corp.internal; location / { proxy_pass http://localhost:3000; } }"),
            }),
            "sites-enabled": dir_node({"default": file_node("# symlink to ../sites-available/default")}),
        }),
        "mysql": dir_node({
            "mysql.conf.d": dir_node({
                "mysqld.cnf": file_node(generate_mysql_conf()),
            }),
            "debian.cnf": file_node(f"[client]\nhost = localhost\nuser = debian-sys-maint\npassword = {rand_str(20)}\nsocket = /var/run/mysqld/mysqld.sock\n"),
        }),
        "postgresql": dir_node({
            "14": dir_node({
                "main": dir_node({
                    "postgresql.conf": file_node("listen_addresses = '10.0.2.10,localhost'\nport = 5432\nmax_connections = 300\nshared_buffers = 2GB\neffective_cache_size = 6GB\nwal_level = replica\nmax_wal_senders = 5\nmax_replication_slots = 5\narchive_mode = on\narchive_command = 'cp %p /var/lib/postgresql/archive/%f'\n"),
                    "pg_hba.conf": file_node("# TYPE  DATABASE USER ADDRESS METHOD\nlocal all all peer\nhost all all 127.0.0.1/32 md5\nhost all all 10.0.0.0/8 md5\nhost replication replicator 10.0.2.0/24 md5\n"),
                })
            })
        }),
        "redis": dir_node({
            "redis.conf": file_node(f"bind 10.0.2.20\nport 6379\nrequirepass {rand_str(24)}\nmaxmemory 2gb\nmaxmemory-policy allkeys-lru\nsave 900 1\nsave 300 10\nappendonly yes\nappendfilename appendonly.aof\n"),
        }),
        "ssl": dir_node({
            "certs": dir_node({
                "corp-ca.crt": file_node("-----BEGIN CERTIFICATE-----\nMIIDxTCCAq2gAwIBAgIQAqxcJmoLQJuPC3nyrkYldTANBgkqhkiG9w0BAQsFADBs\n... (corp internal CA)\n-----END CERTIFICATE-----\n"),
                "svr04.crt": file_node("-----BEGIN CERTIFICATE-----\nMIIDpDCCAoygAwIBAgIBATANBgkqhkiG9w0BAQsFADBsMQswCQYDVQQGEwJVUzEP\n... (server cert)\n-----END CERTIFICATE-----\n"),
            }),
        }),
        "vault.d": dir_node({
            "vault.hcl": file_node("storage \"consul\" {\n  address = \"consul.corp.internal:8500\"\n  path    = \"vault/\"\n  token   = \"" + rand_str(36) + "\"\n}\n\nlistener \"tcp\" {\n  address     = \"0.0.0.0:8200\"\n  tls_cert_file = \"/etc/ssl/certs/svr04.crt\"\n  tls_key_file  = \"/etc/ssl/private/svr04.key\"\n}\n\nui = true\nlog_level = \"info\"\n"),
        }),
        "logrotate.d": dir_node({
            "nginx": file_node("/var/log/nginx/*.log {\n\tdaily\n\tmissingok\n\trotate 14\n\tcompress\n\tdelaycompress\n\tsharedscripts\n\tpostrotate\n\t\t/bin/kill -USR1 $(cat /var/run/nginx.pid)\n\tendscript\n}"),
            "mysql": file_node("/var/log/mysql/*.log {\n\tdaily\n\trotate 7\n\tmissingok\n\tcompress\n\tcreate 640 mysql adm\n}"),
            "syslog": file_node("/var/log/syslog { rotate 7; daily; missingok; notifempty; delaycompress; compress; postrotate /usr/lib/rsyslog/rsyslog-rotate; endscript }"),
        }),
        "kubernetes": dir_node({
            "admin.conf": file_node(f"apiVersion: v1\nclusters:\n- cluster:\n    certificate-authority-data: {rand_str(100)}\n    server: https://10.0.1.10:6443\n  name: corp-k8s\ncontexts:\n- context:\n    cluster: corp-k8s\n    user: corp-admin\n  name: corp-admin@corp-k8s\ncurrent-context: corp-admin@corp-k8s\nkind: Config\nusers:\n- name: corp-admin\n  user:\n    client-certificate-data: {rand_str(100)}\n    client-key-data: {rand_str(100)}\n"),
        }),
        "systemd": dir_node({
            "system": dir_node({
                "nginx.service": file_node("[Unit]\nDescription=nginx HTTP Server\nAfter=network.target\n\n[Service]\nType=forking\nPIDFile=/var/run/nginx.pid\nExecStartPre=/usr/sbin/nginx -t\nExecStart=/usr/sbin/nginx\nExecReload=/bin/kill -s HUP $MAINPID\nPrivateTmp=true\n\n[Install]\nWantedBy=multi-user.target"),
                "app-api.service": file_node("[Unit]\nDescription=Corp Application API\nAfter=network.target mysql.service redis.service\n\n[Service]\nType=simple\nUser=appuser\nWorkingDirectory=/opt/app/api\nExecStart=/usr/bin/python3 /opt/app/api/server.py\nRestart=always\nEnvironmentFile=/opt/app/api/.env\n\n[Install]\nWantedBy=multi-user.target"),
                "prometheus.service": file_node("[Unit]\nDescription=Prometheus Monitoring\nAfter=network.target\n\n[Service]\nUser=prometheus\nExecStart=/opt/prometheus/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus/data --web.listen-address=0.0.0.0:9090\nRestart=always\n\n[Install]\nWantedBy=multi-user.target"),
            })
        }),
        "prometheus": dir_node({
            "prometheus.yml": file_node("global:\n  scrape_interval: 15s\n  evaluation_interval: 15s\n\nalerting:\n  alertmanagers:\n    - static_configs:\n        - targets: ['localhost:9093']\n\nscrape_configs:\n  - job_name: 'prometheus'\n    static_configs:\n      - targets: ['localhost:9090']\n  - job_name: 'node'\n    static_configs:\n      - targets: ['10.0.1.20:9100','10.0.1.21:9100','10.0.1.22:9100','10.0.1.23:9100']\n  - job_name: 'kubernetes-pods'\n    kubernetes_sd_configs:\n      - role: pod\n        namespaces:\n          names: ['default','production','staging']\n"),
        }),
    })

# ─────────────────────────────────────────────
# /root
# ─────────────────────────────────────────────
def generate_root_home():
    return dir_node({
        ".bash_history": file_node(
            "kubectl get pods -A\n"
            "kubectl exec -it db-pod-xyz -- psql -U postgres\n"
            "vault kv get secret/db/prod\n"
            "terraform apply -auto-approve\n"
            "docker ps -a\n"
            "ansible-playbook -i inventory/prod deploy.yml\n"
            "cat /etc/shadow\n"
            "ssh -i ~/.ssh/id_rsa k8s-master-01\n"
            "mysql -h db-primary -u root -p\n"
            "journalctl -xe\n"
            "tail -f /var/log/nginx/error.log\n"
            "grep -r 'CRITICAL' /var/log/\n"
            "netstat -tulnp\n"
            "openssl s_client -connect api.corp.internal:443\n"
            "htop\n"
            "df -h\n"
            "du -sh /var/lib/docker/*\n"
        ),
        ".bashrc": file_node("# Root bashrc\nexport HISTSIZE=10000\nexport HISTFILESIZE=20000\nexport HISTTIMEFORMAT='%F %T '\nalias ll='ls -alF'\nalias k='kubectl'\nalias tf='terraform'\nalias dc='docker-compose'\nexport KUBECONFIG=/etc/kubernetes/admin.conf\nexport VAULT_ADDR=https://vault.corp.internal:8200\nexport VAULT_TOKEN=" + rand_str(36) + "\n"),
        ".ssh": dir_node({
            "id_rsa": file_node("-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAzmHKwNReGNDl15gBNrxV8BsLInkYI4G...(truncated)\n-----END RSA PRIVATE KEY-----"),
            "id_rsa.pub": file_node("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDO... root@svr04"),
            "authorized_keys": file_node("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDO... root@svr04\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDZ... sysadmin@bastion"),
            "known_hosts": file_node("\n".join([f"10.0.1.{i} ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB..." for i in range(10, 30)])),
        }),
        "notes.txt": file_node(
            "# Infrastructure Notes\n\n"
            "## Prod DB password rotation - DUE Friday\n"
            "## K8s cert renewal - expires in 30 days\n"
            "## Vault unseal keys stored in 1Password vault 'INFRA-PROD'\n\n"
            "## Emergency contacts\n"
            "- oncall: +1-555-0192\n"
            "- slack: #infra-alerts\n\n"
            "## Vault root token (TEMP - rotate ASAP): " + rand_str(36) + "\n"
        ),
        "scripts": dir_node({
            "emergency_access.sh": file_node("#!/bin/bash\n# Emergency break-glass script\nset -e\nexport VAULT_TOKEN=" + rand_str(36) + "\nvault kv get secret/emergency/prod-db\nvault kv get secret/emergency/k8s-admin\n"),
            "db_snapshot.sh": file_node("#!/bin/bash\n# Create DB snapshot and upload to S3\nDATE=$(date +%Y%m%d_%H%M%S)\nmysqldump -h db-primary -u root -p\"$DB_ROOT_PASS\" --all-databases | gzip > /tmp/snapshot_$DATE.sql.gz\naws s3 cp /tmp/snapshot_$DATE.sql.gz s3://corp-backups/db/$DATE/\necho 'Snapshot complete: '$DATE\n"),
        }),
        ".vault-token": file_node(rand_str(36)),
        ".aws": dir_node({
            "credentials": file_node(f"[default]\naws_access_key_id = AKIA{rand_str(16).upper()}\naws_secret_access_key = {rand_str(40)}\n\n[prod]\naws_access_key_id = AKIA{rand_str(16).upper()}\naws_secret_access_key = {rand_str(40)}\nregion = us-east-1\n"),
            "config": file_node("[default]\nregion = us-east-1\noutput = json\n\n[profile prod]\nrole_arn = arn:aws:iam::123456789012:role/ProdAdmin\nsource_profile = default\n"),
        }),
    })

# ─────────────────────────────────────────────
# /home/<user>
# ─────────────────────────────────────────────
USER_HISTORIES = {
    "devops": [
        "kubectl get pods -n production", "helm upgrade --install app ./charts/app",
        "terraform plan -var-file=prod.tfvars", "ansible-playbook deploy.yml -i inventory/prod",
        "docker build -t corp/api:latest .", "docker push corp/api:latest",
        "git pull origin main", "git log --oneline -20",
        "ssh k8s-master-01", "journalctl -u app-api -f",
        "kubectl logs -f deployment/api -n production",
        "aws s3 ls s3://corp-backups/", "cat ~/.aws/credentials",
    ],
    "jenkins": [
        "java -version", "service jenkins status",
        "tail -f /var/log/jenkins/jenkins.log",
        "docker build -f Dockerfile.ci -t corp/build-agent .",
        "kubectl create secret generic regcred --from-file=.dockerconfigjson",
    ],
    "dbadmin": [
        "mysql -h db-primary -u root -p", "psql -h db-primary -U postgres",
        "pg_dump -h db-primary -U postgres appdb > backup.sql",
        "mysqlcheck -h db-primary -u root -p --all-databases",
        "redis-cli -h redis-master ping", "redis-cli -h redis-master info replication",
        "cat ~/db_passwords.txt",
    ],
    "sysadmin": [
        "systemctl status nginx", "systemctl restart app-api",
        "journalctl -xe", "dmesg | tail -50",
        "netstat -tulnp", "ss -tlnp",
        "lsof -i :443", "strace -p $(pgrep nginx)",
        "iptables -L -n -v", "cat /var/log/auth.log | tail -100",
        "last -20", "who", "w",
    ],
    "ansible": [
        "ansible all -i inventory/prod -m ping",
        "ansible-playbook site.yml -i inventory/prod --diff",
        "ansible-vault edit group_vars/all/vault.yml",
        "cat ~/.ansible_vault_pass",
    ],
    "terraform": [
        "terraform init", "terraform plan -out=tfplan",
        "terraform apply tfplan", "terraform state list",
        "terraform show", "cat terraform.tfstate | grep -i password",
    ],
    "secops": [
        "grep 'Failed password' /var/log/auth.log | tail -50",
        "fail2ban-client status sshd",
        "lynis audit system", "rkhunter --check",
        "nmap -sV 10.0.1.0/24", "cat /var/log/security_audit.log",
        "openssl x509 -in /etc/ssl/certs/svr04.crt -noout -dates",
    ],
    "dataeng": [
        "python3 etl_pipeline.py", "spark-submit jobs/daily_agg.py",
        "airflow dags list", "airflow tasks run daily_pipeline load_data 2024-01-01",
        "psql -h db-primary -U dataeng -d analyticsdb",
        "aws s3 sync s3://corp-data/raw/ /data/raw/",
        "cat ~/db_creds.env",
    ],
    "mlops": [
        "python3 train.py --config configs/prod.yaml",
        "mlflow runs list", "mlflow models serve -m models:/classifier/production",
        "kubectl apply -f k8s/model-serving.yaml",
        "docker push corp/ml-inference:latest",
        "nvidia-smi", "cat model_registry.json",
    ],
}

def user_bash_history(username):
    specific = USER_HISTORIES.get(username)
    if specific:
        return "\n".join(specific * 2 + random.sample(specific, min(5, len(specific))))
    generic = [
        "ls -la", "pwd", "cd ~", "cat ~/.bashrc",
        "git status", "git pull", "vim .env",
        "sudo systemctl status nginx", "df -h", "free -m",
    ]
    return "\n".join(random.choices(generic, k=random.randint(15, 40)))

def user_env_file(username):
    envs = {
        "devops": f"KUBECONFIG=/home/devops/.kube/config\nAWS_PROFILE=prod\nTF_VAR_env=production\nDOCKER_REGISTRY=registry.corp.internal\n",
        "dbadmin": f"DB_HOST=db-primary.corp.internal\nDB_USER=dbadmin\nDB_PASS={rand_str(16)}\nREDIS_HOST=redis-master.corp.internal\nREDIS_PASS={rand_str(20)}\n",
        "jenkins": f"JENKINS_URL=https://jenkins.corp.internal\nJENKINS_API_TOKEN={rand_hex(32)}\nDOCKER_REGISTRY=registry.corp.internal\n",
        "ansible": f"ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass\nANSIBLE_HOST_KEY_CHECKING=False\n",
        "terraform": f"TF_VAR_db_password={rand_str(20)}\nTF_VAR_aws_region=us-east-1\nAWS_ACCESS_KEY_ID=AKIA{rand_str(16).upper()}\nAWS_SECRET_ACCESS_KEY={rand_str(40)}\n",
        "dataeng": f"DB_CONN=postgresql://dataeng:{rand_str(16)}@db-primary:5432/analyticsdb\nS3_BUCKET=corp-data\nAIRFLOW_HOME=/home/dataeng/airflow\n",
        "mlops": f"MLFLOW_TRACKING_URI=https://mlflow.corp.internal\nMODEL_REGISTRY_URI=s3://corp-models/\nNVIDIA_VISIBLE_DEVICES=all\n",
    }
    return envs.get(username, f"APP_ENV=production\nSECRET_KEY={rand_str(32)}\n")

def generate_user_home(username):
    files = {
        ".bash_history": file_node(user_bash_history(username)),
        ".bashrc": file_node(f"# .bashrc for {username}\nexport HISTSIZE=5000\nexport HISTTIMEFORMAT='%F %T '\nalias ll='ls -alF'\nalias grep='grep --color=auto'\n"),
        ".profile": file_node(f"# ~/.profile for {username}\nexport PATH=$HOME/bin:$HOME/.local/bin:$PATH\n"),
        ".ssh": dir_node({
            "authorized_keys": file_node(f"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD{rand_str(60)}... {username}@workstation"),
            "id_rsa.pub": file_node(f"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD{rand_str(60)}... {username}@svr04"),
            "known_hosts": file_node("\n".join([f"{random_ip(private=True)} ssh-ed25519 AAAAC3Nza..." for _ in range(5)])),
        }),
        ".env": file_node(user_env_file(username)),
    }

    # Add user-specific directories and files
    if username == "devops":
        files["deployments"] = dir_node({
            f"deploy_{app}.sh": file_node(f"#!/bin/bash\nkubectl set image deployment/{app} {app}=registry.corp.internal/{app}:$1 -n production\nkubectl rollout status deployment/{app} -n production\n")
            for app in ["api", "worker", "scheduler", "frontend", "auth-service"]
        })
        files[".kube"] = dir_node({
            "config": file_node(f"apiVersion: v1\nkind: Config\nclusters:\n- name: corp-k8s\n  cluster:\n    server: https://10.0.1.10:6443\n    certificate-authority-data: {rand_str(80)}\nusers:\n- name: devops\n  user:\n    client-certificate-data: {rand_str(80)}\n    client-key-data: {rand_str(80)}\n")
        })
        files[".aws"] = dir_node({
            "credentials": file_node(f"[default]\naws_access_key_id = AKIA{rand_str(16).upper()}\naws_secret_access_key = {rand_str(40)}\n\n[prod]\naws_access_key_id = AKIA{rand_str(16).upper()}\naws_secret_access_key = {rand_str(40)}\n"),
        })

    elif username == "dbadmin":
        files["db_passwords.txt"] = file_node(
            f"# DB Credentials - DO NOT SHARE\n"
            f"MySQL root: {rand_str(16)}\n"
            f"PostgreSQL postgres: {rand_str(16)}\n"
            f"Redis auth: {rand_str(20)}\n"
            f"App DB user: {rand_str(14)}\n"
        )
        files["backups"] = dir_node({
            f"backup_{i}.sql.gz.note": file_node(f"Backup created {timestamp(i*1440)} - size ~2.4GB")
            for i in range(7)
        })

    elif username == "ansible":
        files[".vault_pass"] = file_node(rand_str(40))
        files["inventory"] = dir_node({
            "prod": file_node("[k8s_masters]\n10.0.1.10 ansible_user=ansible\n10.0.1.11 ansible_user=ansible\n\n[k8s_workers]\n10.0.1.20\n10.0.1.21\n10.0.1.22\n\n[databases]\n10.0.2.10 ansible_user=ansible\n\n[all:vars]\nansible_python_interpreter=/usr/bin/python3\n"),
            "staging": file_node("[k8s_workers]\n10.1.1.20\n10.1.1.21\n\n[databases]\n10.1.2.10\n"),
        })
        files["group_vars"] = dir_node({
            "all": dir_node({
                "vault.yml": file_node(f"$ANSIBLE_VAULT;1.1;AES256\n{rand_hex(200)}\n"),
                "vars.yml": file_node("env: production\ndomain: corp.internal\nregistry: registry.corp.internal\n"),
            })
        })

    elif username == "terraform":
        files["infra"] = dir_node({
            "main.tf": file_node('provider "aws" {\n  region = var.aws_region\n}\n\nmodule "vpc" {\n  source = "./modules/vpc"\n  cidr = "10.0.0.0/8"\n}\n\nmodule "k8s" {\n  source = "./modules/eks"\n  cluster_name = "corp-prod"\n  node_count = 10\n}\n'),
            "terraform.tfstate": file_node(f'{{"version": 4, "terraform_version": "1.6.0", "resources": [{{"type": "aws_instance", "name": "svr04", "instances": [{{"attributes": {{"id": "i-{rand_hex(17)}", "ami": "ami-0c55b159cbfafe1f0", "instance_type": "t3.xlarge", "private_ip": "10.0.1.100"}}}}]}}]}}'),
            "secrets.tfvars": file_node(f"db_password = \"{rand_str(20)}\"\nredis_password = \"{rand_str(20)}\"\njwt_secret = \"{rand_str(32)}\"\n"),
        })

    elif username == "jenkins":
        files["workspace"] = dir_node({
            "api-pipeline": dir_node({
                "Jenkinsfile": file_node("pipeline {\n  agent any\n  stages {\n    stage('Build') { steps { sh 'docker build -t corp/api:${BUILD_NUMBER} .' } }\n    stage('Test') { steps { sh 'pytest tests/' } }\n    stage('Push') { steps { sh 'docker push corp/api:${BUILD_NUMBER}' } }\n    stage('Deploy') { steps { sh './deploy.sh ${BUILD_NUMBER}' } }\n  }\n}\n"),
            }),
        })
        files[".docker"] = dir_node({
            "config.json": file_node(f'{{"auths": {{"registry.corp.internal": {{"auth": "{rand_str(60)}"}}}}}}'),
        })

    elif username == "secops":
        files["reports"] = dir_node({
            f"audit_{2026 if i < 3 else 2025}_{str(i).zfill(2)}.txt": file_node(f"Security Audit Report\nDate: {timestamp(i*30*24*60)}\nScore: {random.randint(72,96)}/100\nFindings: {random.randint(0, 8)} medium, {random.randint(0,3)} high\nRemediated: {random.randint(1,5)}\n")
            for i in range(1, 13)
        })
        files["scripts"] = dir_node({
            "scan_hosts.sh": file_node("#!/bin/bash\nfor host in $(cat hosts.txt); do\n  nmap -sV -O $host >> scan_results.txt\ndone\n"),
            "check_certs.sh": file_node("#!/bin/bash\nfor cert in /etc/ssl/certs/*.crt; do\n  openssl x509 -in $cert -noout -enddate\ndone\n"),
        })

    elif username == "dataeng":
        files["pipelines"] = dir_node({
            "daily_etl.py": file_node("import pandas as pd\nfrom sqlalchemy import create_engine\nimport os\n\nDB_CONN = os.environ['DB_CONN']\nengine = create_engine(DB_CONN)\n\ndef run():\n    df = pd.read_sql('SELECT * FROM events WHERE date = CURRENT_DATE', engine)\n    df.to_parquet(f's3://corp-data/processed/{pd.Timestamp.now().date()}.parquet')\n    print(f'Processed {len(df)} rows')\n\nif __name__ == '__main__': run()\n"),
            "db_creds.env": file_node(f"DB_HOST=db-primary.corp.internal\nDB_USER=dataeng\nDB_PASS={rand_str(18)}\nDB_NAME=analyticsdb\n"),
        })

    return dir_node(files)

def generate_home():
    users = {}
    for u in USERS:
        users[u] = generate_user_home(u)
    return dir_node(users)

# ─────────────────────────────────────────────
# /var
# ─────────────────────────────────────────────
def generate_auth_log():
    lines = []
    now = datetime.now()
    events = [
        ("Accepted publickey for {u} from {ip} port {p} ssh2", 40),
        ("Failed password for {u} from {ip} port {p} ssh2", 30),
        ("Invalid user {u} from {ip} port {p}", 20),
        ("pam_unix(sshd:session): session opened for user {u}", 20),
        ("Disconnected from {ip} port {p} [preauth]", 15),
        ("PAM 3 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}", 10),
        ("sudo: {u} : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND=/bin/bash", 8),
    ]
    for _ in range(500):
        t = now - timedelta(minutes=random.randint(1, 43200))
        tmpl, _ = random.choices([e[0] for e in events], weights=[e[1] for e in events])[0], None
        tmpl = events[random.randrange(len(events))][0]
        line = tmpl.format(
            u=random.choice(USERS + ["root", "admin", "test", "oracle", "pi"]),
            ip=random_ip(),
            p=rand_port()
        )
        lines.append(f"{t.strftime('%b %d %H:%M:%S')} svr04 sshd[{random.randint(1000,9999)}]: {line}")
    lines.sort()
    return "\n".join(lines)

def generate_syslog():
    components = ["kernel", "systemd", "nginx", "mysqld", "redis-server", "cron", "rsyslogd", "dockerd", "kubelet", "prometheus"]
    messages = [
        "Started {c} service.", "Stopped {c} service.",
        "CPU: {n}% idle", "OOM score adjusted",
        "iptables: new connection from {ip}",
        "disk I/O spike detected on /dev/sda1",
        "systemd: Unit {c}.service entered failed state",
        "Synchronized to time server {ip}",
    ]
    lines = []
    now = datetime.now()
    for _ in range(400):
        t = now - timedelta(minutes=random.randint(1, 10080))
        c = random.choice(components)
        msg = random.choice(messages).format(c=c, ip=random_ip(private=True), n=random.randint(5, 95))
        lines.append(f"{t.strftime('%b %d %H:%M:%S')} svr04 {c}[{random.randint(100,9999)}]: {msg}")
    lines.sort()
    return "\n".join(lines)

def generate_nginx_access_log():
    paths = ["/", "/api/v1/users", "/api/v1/health", "/api/v2/data", "/admin", "/login",
             "/metrics", "/static/js/app.js", "/.env", "/wp-admin/", "/phpinfo.php",
             "/api/v1/products", "/api/v1/orders", "/dashboard"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    codes = [200]*40 + [201]*10 + [301]*5 + [302]*5 + [400]*5 + [401]*8 + [403]*5 + [404]*10 + [500]*3
    lines = []
    now = datetime.now()
    for _ in range(600):
        t = now - timedelta(minutes=random.randint(1, 10080))
        ip = random_ip()
        method = random.choice(methods)
        path = random.choice(paths)
        code = random.choice(codes)
        size = random.randint(100, 50000)
        ua = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'curl/7.81.0', 'python-requests/2.28.1', 'Go-http-client/1.1',
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'masscan/1.0 (https://github.com/robertdavidgraham/masscan)',
            'zgrab/0.x', 'Nmap Scripting Engine',
        ])
        lines.append(f'{ip} - - [{t.strftime("%d/%b/%Y:%H:%M:%S")} +0000] "{method} {path} HTTP/1.1" {code} {size} "-" "{ua}"')
    return "\n".join(lines)

def generate_var():
    return dir_node({
        "log": dir_node({
            "auth.log": file_node(generate_auth_log()),
            "auth.log.1": file_node(generate_auth_log()),
            "syslog": file_node(generate_syslog()),
            "syslog.1": file_node(generate_syslog()),
            "kern.log": file_node("\n".join([f"{timestamp(i*10)} svr04 kernel: [  {i*10}.000000] {'EXT4-fs' if i%3==0 else 'TCP'}: {'journal commit' if i%3==0 else f'connection from {random_ip()}'}" for i in range(100)])),
            "dpkg.log": file_node("\n".join([f"{timestamp(i*60*24)} status installed {pkg}:{random.choice(['amd64','all'])}" for i, pkg in enumerate(["nginx","mysql-server","redis","docker-ce","kubectl","python3","git","curl","vim","htop","fail2ban","auditd","lynis","prometheus-node-exporter","certbot"])])),
            "nginx": dir_node({
                "access.log": file_node(generate_nginx_access_log()),
                "error.log": file_node("\n".join([f"{timestamp(i*15)} [error] {random.randint(1,5)}#{random.randint(1,100)}: *{i} {random.choice(['connect() failed','upstream timed out','no live upstreams','SSL_do_handshake() failed'])} while connecting to upstream, client: {random_ip()}, server: api.corp.internal" for i in range(60)])),
            }),
            "mysql": dir_node({
                "error.log": file_node("\n".join([f"{timestamp(i*30)} {random.randint(1,100)} [Note] {random.choice(['InnoDB: page_cleaner took','Aborted connection','Access denied for user','Slave SQL thread initialized'])}" for i in range(80)])),
                "mysql-bin.000001": file_node("(binary log data - use mysqlbinlog to read)"),
            }),
            "security_audit.log": file_node("\n".join([f"{timestamp(i*1440)} [{'PASS' if random.random()>0.2 else 'FAIL'}] Check: {check}" for i, check in enumerate(["SSH config hardening","Sudo privileges audit","Open ports scan","File permissions","User account review","Password policy","Firewall rules","SSL certificate validity","Kernel security params","Service inventory"])])),
            "sudo.log": file_node("\n".join([f"{timestamp(i*60)} COMMAND={random.choice(['/bin/bash','/bin/cat /etc/shadow','/usr/local/bin/kubectl','docker ps','/sbin/iptables -L'])} user={random.choice(['devops','sysadmin','ansible'])} tty=pts/0" for i in range(80)])),
            "fail2ban.log": file_node("\n".join([f"{timestamp(i*5)} fail2ban.filter [INFO] Found {random_ip()} - {random.randint(1,10)} attempts" for i in range(200)])),
            "certbot.log": file_node("\n".join([f"{timestamp(i*10080)} Cert not yet due for renewal" for i in range(4)] + ["Renewing certificate for api.corp.internal\nCertificate successfully renewed\n"])),
            "db_backup.log": file_node("\n".join([f"{timestamp(i*1440)} DB backup {'SUCCESS' if random.random()>0.05 else 'FAILED'} size={random.randint(1,5)}GB duration={random.randint(2,15)}min" for i in range(14)])),
        }),
        "www": dir_node({
            "html": dir_node({
                "index.php": file_node("<?php\nrequire_once 'config.php';\nrequire_once 'vendor/autoload.php';\n$app = new App\\Application();\n$app->run();\n"),
                "config.php": file_node(f"<?php\ndefine('DB_HOST', 'db-primary.corp.internal');\ndefine('DB_USER', 'appuser');\ndefine('DB_PASS', '{rand_str(18)}');\ndefine('DB_NAME', 'appdb');\ndefine('REDIS_HOST', 'redis-master.corp.internal');\ndefine('REDIS_PASS', '{rand_str(20)}');\ndefine('JWT_SECRET', '{rand_str(32)}');\ndefine('APP_ENV', 'production');\ndefine('AWS_KEY', 'AKIA{rand_str(16).upper()}');\ndefine('AWS_SECRET', '{rand_str(40)}');\n"),
                ".htaccess": file_node("RewriteEngine On\nRewriteRule ^(.*)$ index.php [QSA,L]\nOptions -Indexes\nOrder deny,allow\nDeny from all\nAllow from 10.0.0.0/8\n"),
                "uploads": dir_node({f"file_{i}.png": file_node("(binary image data)") for i in range(10)}),
            }),
        }),
        "lib": dir_node({
            "mysql": dir_node({"ibdata1": file_node("(InnoDB system tablespace)")}),
            "postgresql": dir_node({"14": dir_node({"main": dir_node({"PG_VERSION": file_node("14")})})}),
            "redis": dir_node({"dump.rdb": file_node("REDIS0011 (binary RDB snapshot)")}),
            "docker": dir_node({
                "containers": dir_node({
                    f"container_{rand_hex(12)}": dir_node({
                        "config.v2.json": file_node(f'{{"Image": "corp/{svc}:latest", "Created": "{timestamp(random.randint(1,10000))}"}}')
                    })
                    for svc in ["api", "worker", "scheduler", "frontend", "redis", "nginx-proxy"]
                }),
            }),
        }),
        "backups": dir_node({
            f"db_{i}.sql.gz": file_node(f"(compressed SQL dump created {timestamp(i*1440)})")
            for i in range(7)
        }),
        "cache": dir_node({
            "apt": dir_node({"archives": dir_node({})}),
        }),
    })

# ─────────────────────────────────────────────
# /opt
# ─────────────────────────────────────────────
MICROSERVICES = [
    "api-gateway", "auth-service", "user-service", "order-service", "payment-service",
    "notification-service", "inventory-service", "analytics-service", "report-service",
    "search-service", "recommendation-engine", "email-service", "sms-service",
    "file-service", "billing-service", "subscription-service", "webhook-service",
    "audit-service", "config-service", "session-service",
]

def generate_service(name):
    return dir_node({
        "src": dir_node({
            "main.py": file_node(f"#!/usr/bin/env python3\n# {name}\nimport os, logging\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\nlogging.basicConfig(level=logging.INFO)\n\n@app.route('/health')\ndef health(): return jsonify(status='ok', service='{name}')\n\n@app.route('/api/v1/status')\ndef status(): return jsonify(service='{name}', version='1.0.0', env=os.getenv('APP_ENV'))\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))\n"),
            "config.py": file_node(f"# {name} configuration\nimport os\nDB_HOST = os.getenv('DB_HOST', 'db-primary.corp.internal')\nDB_PASS = os.getenv('DB_PASS', '')\nREDIS_HOST = os.getenv('REDIS_HOST', 'redis-master.corp.internal')\nJWT_SECRET = os.getenv('JWT_SECRET', '')\n"),
            "models.py": file_node(f"# Data models for {name}\nfrom sqlalchemy import Column, Integer, String, DateTime\nfrom database import Base\n\nclass Record(Base):\n    __tablename__ = 'records'\n    id = Column(Integer, primary_key=True)\n    name = Column(String(255))\n    created_at = Column(DateTime)\n"),
        }),
        "Dockerfile": file_node(f"FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY src/ .\nEXPOSE 8080\nCMD [\"python3\", \"main.py\"]\n"),
        "docker-compose.yml": file_node(f"version: '3.8'\nservices:\n  {name}:\n    image: corp/{name}:latest\n    ports:\n      - \"8080:8080\"\n    environment:\n      - APP_ENV=production\n      - DB_HOST=db-primary.corp.internal\n      - DB_PASS=${{DB_PASS}}\n      - JWT_SECRET=${{JWT_SECRET}}\n    restart: always\n"),
        ".env": file_node(f"APP_ENV=production\nDB_HOST=db-primary.corp.internal\nDB_PASS={rand_str(18)}\nREDIS_HOST=redis-master.corp.internal\nREDIS_PASS={rand_str(20)}\nJWT_SECRET={rand_str(32)}\nAPI_KEY={rand_str(32)}\nPORT=8080\nLOG_LEVEL=info\n"),
        "requirements.txt": file_node("flask==3.0.0\nflask-sqlalchemy==3.1.1\nflask-redis==0.4.0\nrequests==2.31.0\npyjwt==2.8.0\npsycopg2-binary==2.9.9\nredis==5.0.1\ngunicorn==21.2.0\nprometheus-client==0.19.0\n"),
        "README.md": file_node(f"# {name}\n\nPart of the corp microservices platform.\n\n## Running\n```\ndocker-compose up -d\n```\n\n## Endpoints\n- GET /health\n- GET /api/v1/status\n"),
    })

def generate_opt():
    services = {svc: generate_service(svc) for svc in MICROSERVICES}
    return dir_node({
        "app": dir_node(services),
        "scripts": dir_node({
            "db_backup.sh": file_node(f"#!/bin/bash\nset -e\nDATE=$(date +%Y%m%d_%H%M%S)\nDB_PASS='{rand_str(18)}'\nmysqldump -h db-primary -u root -p\"$DB_PASS\" --all-databases | gzip > /var/backups/db_$DATE.sql.gz\naws s3 cp /var/backups/db_$DATE.sql.gz s3://corp-backups/db/$DATE/\necho '[OK] Backup uploaded: '$DATE\n"),
            "s3_sync.sh": file_node("#!/bin/bash\naws s3 sync /var/backups/ s3://corp-backups/manual/ --storage-class STANDARD_IA\necho '[OK] S3 sync complete'\n"),
            "health_check.sh": file_node("#!/bin/bash\nfor svc in api-gateway auth-service user-service order-service; do\n  STATUS=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/health)\n  [ \"$STATUS\" != \"200\" ] && echo \"[ALERT] $svc unhealthy\" | mail -s \"Health Alert\" ops@corp.internal\ndone\n"),
            "deploy.sh": file_node("#!/bin/bash\n# Rolling deploy\nSERVICE=$1\nTAG=$2\nkubectl set image deployment/$SERVICE $SERVICE=registry.corp.internal/$SERVICE:$TAG -n production\nkubectl rollout status deployment/$SERVICE -n production --timeout=300s\necho \"[OK] Deployed $SERVICE:$TAG\"\n"),
            "audit_scan.sh": file_node("#!/bin/bash\n# Daily security scan\nlynis audit system --quiet >> /var/log/security_audit.log\nrkhunter --check --sk >> /var/log/security_audit.log\nfind / -perm -4000 -type f 2>/dev/null >> /var/log/security_audit.log\necho '[OK] Audit complete'\n"),
            "rotate_secrets.sh": file_node(f"#!/bin/bash\n# Secret rotation script\nNEW_DB_PASS=$(openssl rand -base64 24)\nNEW_REDIS_PASS=$(openssl rand -base64 24)\nvault kv put secret/db/prod password=$NEW_DB_PASS\nvault kv put secret/redis/prod password=$NEW_REDIS_PASS\nmysql -h db-primary -u root -p\"{rand_str(18)}\" -e \"ALTER USER 'appuser'@'%' IDENTIFIED BY '$NEW_DB_PASS';\"\nkubectl create secret generic db-credentials --from-literal=password=$NEW_DB_PASS --dry-run=client -o yaml | kubectl apply -f -\necho '[OK] Secrets rotated'\n"),
        }),
        "prometheus": dir_node({
            "prometheus": file_node("(prometheus binary)"),
            "promtool": file_node("(promtool binary)"),
            "rules": dir_node({
                "alerts.yml": file_node("groups:\n- name: corp_alerts\n  rules:\n  - alert: HighCPU\n    expr: 100 - (avg by(instance)(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100) > 85\n    for: 5m\n    labels:\n      severity: warning\n  - alert: DiskAlmostFull\n    expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10\n    for: 1m\n    labels:\n      severity: critical\n  - alert: ServiceDown\n    expr: up == 0\n    for: 1m\n    labels:\n      severity: critical\n"),
            }),
        }),
        "vault": dir_node({
            "vault": file_node("(vault binary)"),
        }),
        "consul": dir_node({
            "consul": file_node("(consul binary)"),
            "config.json": file_node(f'{{"datacenter": "dc1", "data_dir": "/var/lib/consul", "encrypt": "{rand_str(32)}", "retry_join": ["10.0.3.15"], "ui_config": {{"enabled": true}}, "acl": {{"enabled": true, "default_policy": "deny"}}}}'),
        }),
        "k8s-tools": dir_node({
            "manifests": dir_node({
                ns: dir_node({
                    f"{svc}-deployment.yaml": file_node(f"apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: {svc}\n  namespace: {ns}\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: {svc}\n  template:\n    metadata:\n      labels:\n        app: {svc}\n    spec:\n      containers:\n      - name: {svc}\n        image: registry.corp.internal/{svc}:latest\n        ports:\n        - containerPort: 8080\n        envFrom:\n        - secretRef:\n            name: app-secrets\n")
                    for svc in MICROSERVICES[:10]
                })
                for ns in ["production", "staging", "monitoring"]
            }),
        }),
        "data": dir_node({
            "models": dir_node({
                f"model_v{v}.pkl": file_node(f"(serialized ML model v{v} - created {timestamp(v*1440)})")
                for v in range(1, 8)
            }),
            "datasets": dir_node({
                f"dataset_{d}.parquet": file_node(f"(Parquet dataset - {random.randint(100000, 5000000)} rows)")
                for d in ["users", "events", "orders", "products", "sessions", "clicks", "impressions"]
            }),
        }),
    })

# ─────────────────────────────────────────────
# /proc (fake)
# ─────────────────────────────────────────────
def generate_proc():
    return dir_node({
        "version": file_node("Linux version 5.15.0-91-generic (buildd@lcy02-amd64-059) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023"),
        "cpuinfo": file_node("\n".join([f"processor\t: {i}\nvendor_id\t: GenuineIntel\ncpu family\t: 6\nmodel\t\t: 85\nmodel name\t: Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz\ncpu MHz\t\t: {random.uniform(800,3500):.3f}\ncache size\t: 36608 KB\ncpu cores\t: 16\n" for i in range(8)])),
        "meminfo": file_node("MemTotal:       65536000 kB\nMemFree:        12048192 kB\nMemAvailable:   45032448 kB\nBuffers:         1048576 kB\nCached:         24576000 kB\nSwapTotal:       4194304 kB\nSwapFree:        4194304 kB\n"),
        "net": dir_node({
            "arp": file_node("IP address       HW type     Flags       HW address            Mask     Device\n10.0.1.10        0x1         0x2         02:42:0a:00:01:0a     *        eth0\n10.0.1.11        0x1         0x2         02:42:0a:00:01:0b     *        eth0\n10.0.2.10        0x1         0x2         02:42:0a:00:02:0a     *        eth0\n"),
            "tcp": file_node("  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n   0: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 12345 1 0000000000000000 100 0 0 10 0\n   1: 00000000:01BB 00000000:0000 0A 00000000:00000000 00:00000000 00000000    33        0 23456 1 0000000000000000 100 0 0 10 0\n"),
        }),
        "uptime": file_node(f"{random.randint(100000,2000000)}.00 {random.randint(50000,1000000)}.00"),
    })

# ─────────────────────────────────────────────
# /dev & /sys (minimal)
# ─────────────────────────────────────────────
def generate_dev():
    return dir_node({
        "null": file_node(""),
        "zero": file_node(""),
        "random": file_node(""),
        "urandom": file_node(""),
        "sda": file_node("(block device)"),
        "sda1": file_node("(block device partition 1)"),
        "sdb": file_node("(block device - /data)"),
    })

def generate_sys():
    return dir_node({
        "kernel": dir_node({
            "hostname": file_node("svr04.corp.internal"),
            "ostype": file_node("Linux"),
            "osrelease": file_node("5.15.0-91-generic"),
            "version": file_node("#101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023"),
            "dmesg": file_node("(kernel ring buffer - use dmesg command)"),
        }),
        "class": dir_node({
            "net": dir_node({
                "eth0": dir_node({
                    "address": file_node("02:42:0a:00:01:64"),
                    "speed": file_node("10000"),
                    "operstate": file_node("up"),
                }),
            }),
        }),
    })

# ─────────────────────────────────────────────
# /tmp
# ─────────────────────────────────────────────
def generate_tmp():
    tmp = {}
    for i in range(50):
        tmp[f"tmp_{rand_hex(8)}.tmp"] = file_node("(temporary data)")
    tmp["systemd-private-abc123"] = dir_node({"tmp": dir_node({})})
    tmp[".X11-unix"] = dir_node({})
    tmp["ansible_tmp"] = dir_node({
        f"ansible_{rand_hex(8)}": dir_node({"AnsiballZ_command.py": file_node("# Ansible temp module")})
        for _ in range(3)
    })
    tmp["snap-private-tmp"] = dir_node({})
    return dir_node(tmp)

# ─────────────────────────────────────────────
# /usr & /bin (stubs)
# ─────────────────────────────────────────────
def generate_usr():
    return dir_node({
        "local": dir_node({
            "bin": dir_node({
                "kubectl": file_node("(kubectl binary v1.28.4)"),
                "helm": file_node("(helm binary v3.13.0)"),
                "terraform": file_node("(terraform binary v1.6.4)"),
                "ansible": file_node("(ansible binary v2.15.0)"),
                "vault": file_node("(vault binary v1.15.2)"),
                "consul": file_node("(consul binary v1.17.0)"),
            }),
            "lib": dir_node({}),
            "share": dir_node({}),
        }),
        "bin": dir_node({b: file_node(f"(system binary: {b})") for b in ["python3","python3.11","bash","sh","curl","wget","vim","git","jq","htop","strace","tcpdump","nmap","openssl","rsync","tar","gzip","awk","sed"]}),
        "sbin": dir_node({b: file_node(f"(sbin binary: {b})") for b in ["nginx","iptables","ip","tcpdump","sshd","logrotate","adduser","useradd","groupadd"]}),
        "share": dir_node({
            "doc": dir_node({pkg: dir_node({"README": file_node(f"Documentation for {pkg}")}) for pkg in ["nginx","mysql-server","redis","docker-ce","kubectl","fail2ban","auditd"]}),
        }),
    })

def generate_bin():
    return dir_node({b: file_node(f"(binary: {b})") for b in ["bash","sh","ls","cat","cd","pwd","mkdir","rmdir","rm","cp","mv","touch","echo","grep","find","ps","kill","top","df","du","mount","umount","date","hostname","uname","id","whoami","su","sudo"]})

# ─────────────────────────────────────────────
# /data (NFS-mounted corporate share)
# ─────────────────────────────────────────────
def generate_data():
    return dir_node({
        "shared": dir_node({
            "finance": dir_node({
                f"Q{q}_{y}_report.xlsx": file_node(f"(Excel report Q{q} {y} - confidential)")
                for q in range(1, 5) for y in [2024, 2025]
            }),
            "hr": dir_node({
                "employee_list.csv": file_node("employee_id,name,email,department,salary\n1001,John Smith,j.smith@corp.com,Engineering,125000\n1002,Sarah Johnson,s.johnson@corp.com,Finance,98000\n..."),
                "org_chart.pdf": file_node("(PDF org chart)"),
                "policies": dir_node({p: file_node(f"(policy document: {p})") for p in ["remote_work_policy.pdf","security_policy.pdf","acceptable_use.pdf","incident_response.pdf"]}),
            }),
            "engineering": dir_node({
                "architecture": dir_node({
                    f"{doc}.pdf": file_node(f"(Architecture document: {doc})")
                    for doc in ["system_overview","network_topology","k8s_design","database_schema","api_spec_v3","security_model","dr_plan"]
                }),
                "runbooks": dir_node({
                    f"{rb}.md": file_node(f"# {rb} Runbook\n\n## Steps\n1. Check service status\n2. Review logs\n3. Escalate if needed\n")
                    for rb in ["db_failover","k8s_node_drain","ssl_cert_renewal","incident_response","on_call_handoff","scale_out","rollback_procedure"]
                }),
            }),
        }),
        "raw": dir_node({
            f"events_{2025}_{str(m).zfill(2)}.parquet": file_node(f"(Parquet - ~{random.randint(50,500)}M rows)")
            for m in range(1, 13)
        }),
    })

# ─────────────────────────────────────────────
# ASSEMBLE FILESYSTEM
# ─────────────────────────────────────────────
def generate_filesystem():
    return {
        "/": dir_node({
            "etc":  generate_etc(),
            "home": generate_home(),
            "root": generate_root_home(),
            "var":  generate_var(),
            "opt":  generate_opt(),
            "tmp":  generate_tmp(),
            "proc": generate_proc(),
            "dev":  generate_dev(),
            "sys":  generate_sys(),
            "usr":  generate_usr(),
            "bin":  generate_bin(),
            "sbin": dir_node({b: file_node(f"(sbin: {b})") for b in ["iptables","ip","sshd","nginx","modprobe","fdisk","mkfs","mount"]}),
            "lib":  dir_node({"x86_64-linux-gnu": dir_node({}), "systemd": dir_node({"systemd": file_node("(systemd binary)")})}),
            "mnt":  dir_node({"nfs": dir_node({"README": file_node("NFS mount point - run: mount 10.0.5.10:/exports/shared /mnt/nfs")})}),
            "media": dir_node({}),
            "srv":  dir_node({"http": dir_node({}), "ftp": dir_node({})}),
            "run":  dir_node({"nginx.pid": file_node(str(random.randint(1000,9999))), "sshd.pid": file_node(str(random.randint(1000,9999))), "docker.sock": file_node("(Unix socket)")}),
            "data": generate_data(),
            "boot": dir_node({
                "vmlinuz": file_node("(compressed kernel image)"),
                "initrd.img": file_node("(initial ramdisk)"),
                "grub": dir_node({
                    "grub.cfg": file_node("set default=0\nset timeout=5\nmenuentry 'Ubuntu' { linux /boot/vmlinuz root=UUID=a6c6-b4f2 ro quiet splash }")
                }),
            }),
        })
    }

def main():
    print("[*] Generating enterprise filesystem...")
    fs = generate_filesystem()
    print("[*] Writing filesystem.yaml ...")
    with open(OUTPUT, "w") as f:
        yaml.dump(fs, f, sort_keys=False)
    import os
    size = os.path.getsize(OUTPUT) / 1024
    print(f"[+] Done. filesystem.yaml written ({size:.1f} KB)")

if __name__ == "__main__":
    main()
