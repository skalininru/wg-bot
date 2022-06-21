import subprocess
import ipaddress
from string import Template
from loguru import logger
from sqlalchemy.orm import Session

import config
from schemas import WGUserCreate
from crud import wg_user as db_wg_user


def generate_keys():
    private_key = subprocess.check_output(["wg", "genkey"])
    public_key = subprocess.check_output(
        ["wg", "pubkey"],
        input=private_key
    )

    private_key = private_key.decode("utf-8").strip()
    public_key = public_key.decode("utf-8").strip()
    return dict(
        private_key=private_key,
        public_key=public_key
    )


def get_free_ip(db: Session):
    wg_network = ipaddress.IPv4Network(config.SERVER_NETWORK)
    wg_hosts = wg_network.hosts()
    _ = next(wg_hosts)
    wg_user_list = db_wg_user.get_wguser_list(db)

    if len(wg_user_list) > 0:
        used_ip_list = []
        for user in wg_user_list:
            used_ip_list.append(user.ip_address)
        logger.debug(f"Used adresses:\n{used_ip_list}")
        hosts_iterator = (
            host for host in wg_hosts if str(host) not in set(used_ip_list)
        )
        free_ip_address = next(hosts_iterator)
    else:
        free_ip_address = next(wg_hosts)

    logger.debug(f"Found free ip: {free_ip_address}")
    return free_ip_address


def get_wg_user(db: Session, wg_user_name):
    wg_user_keys = generate_keys()
    wg_user = WGUserCreate(
        name=wg_user_name,
        ip_address=get_free_ip(db),
        public_key=wg_user_keys['public_key'],
        private_key=wg_user_keys['private_key']
    )
    wg_user_cmd = [
        "wg", "set", config.SERVER_INTERFACE,
        "peer", wg_user.public_key,
        "allowed-ips", str(wg_user.ip_address)
    ]
    subprocess.check_call(wg_user_cmd)
    return wg_user


def get_user_config(wg_user: WGUserCreate):
    template_config = {
        "client_ip": wg_user.ip_address,
        "client_private_key": wg_user.private_key,
        "wg_public_key": config.SERVER_PUBLIC_KEY,
        "wg_endpoint": config.SERVER_ENDPOINT
    }
    with open("client_config.template", "r") as f:
        src = Template(f.read())
        result = src.substitute(template_config)
        return result


def remove_wg_user(db: Session, username):
    wg_user = db_wg_user.get_wguser_by_name(db, username)
    wg_user_cmd = [
        "wg", "set", config.SERVER_INTERFACE,
        "peer", wg_user.public_key,
        "remove"
    ]
    logger.debug(f"remove user cmd: {wg_user_cmd}")
    remove_user_result = subprocess.check_output(wg_user_cmd)
    logger.debug(f"Result: {remove_user_result}")
    db_wg_user.remove_wguser(db, username)
