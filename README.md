# 🐉🤖 wg-bot: Wireguard telegram bot

Telegram bot for Wireguard VPN user management

# Features
- Managing WireGuard peers:
  - add peer
  - remove peer
  - show list of added peers
- Retrieve configs as file: 
  - quick and easy import into the wireguard client
  - quick and easy forward config to someone else
- Admin user
  - only admin user can manage wireguard peers

# Usage
Just write a message to the bot.
Available comands:
- `/get_users`: show active users
- `/add_user`: add new user
- `/get_user_config`: get wireguard config file
- `/remove_user`: remove existing user
- `/about_me`: show your profile
- `/help`: show help message

# Installation and configuration
- Install wireguard
```bash
apt update -y && apt upgrade -y
apt install vim htop curl git iptables wireguard -y
cd /etc/wireguard
wg genkey > private.key
chmod 600 private.key
wg pubkey < private.key > public.key
cat private.key
vim wg0.conf
:::
[Interface]
PrivateKey = $$$PRIVATE_KEY$$$
Address = 10.0.0.1/24
SaveConfig = true
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
ListenPort = 51820
:::
vim /etc/sysctl.conf
sysctl -p
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0
```
- Install and configure PostgreSQL database
```bash
apt install postgresql postgresql-contrib libpq-dev -y
su postgres
psql
create database wga;
create user u_wga with encrypted password 'mySuperPassw0rd!';
grant all privileges on database wga to u_wga;
```

- Install and configure wg-bot
```bash
apt install python3-pip
pip install --upgrade pip
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
source $HOME/.poetry/env
poetry completions bash > /etc/bash_completion.d/poetry.bash-completion
cd /opt
mkdir wg-admin
cd wg-admin
git clone https://github.com/skalininru/wg-bot.git
```