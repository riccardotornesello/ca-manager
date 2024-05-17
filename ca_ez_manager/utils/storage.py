import os
from typing import List

from ca_ez_manager.utils.crypto import (
    save_private_key,
    save_certificate,
    save_csr,
    load_private_key,
    load_certificate,
)


# TODO: allow custom directory
user_home = os.path.expanduser("~")
ca_folder = os.path.join(user_home, ".ca")

NECESSARY_CA_FILES = ["ca.key", "ca.pem"]


def init_storage():
    if not os.path.exists(ca_folder):
        os.makedirs(ca_folder)


def get_ca_list() -> List[str]:
    init_storage()

    # Get the list of subdirectories in the CA folder
    subdirs = os.listdir(ca_folder)

    # Filter out only the directories
    subdirs = [d for d in subdirs if os.path.isdir(f"{ca_folder}/{d}")]

    # Return only the directories that contain the necessary files
    return [d for d in subdirs if all(os.path.exists(f"{ca_folder}/{d}/{fn}") for fn in NECESSARY_CA_FILES)]


def store_ca(ca_name: str, private_key, cert):
    os.makedirs(f"{ca_folder}/{ca_name}")

    save_private_key(private_key, f"{ca_folder}/{ca_name}/ca.key")
    save_certificate(cert, f"{ca_folder}/{ca_name}/ca.pem")


def get_ca(ca_name: str):
    for fn in NECESSARY_CA_FILES:
        if not os.path.exists(f"{ca_folder}/{ca_name}/{fn}"):
            raise FileNotFoundError(f"CA {ca_name} not found")

    private_key = load_private_key(f"{ca_folder}/{ca_name}/ca.key")
    cert = load_certificate(f"{ca_folder}/{ca_name}/ca.pem")

    return private_key, cert


def store_cert(ca_name: str, cert_name: str, private_key, cert, csr):
    os.makedirs(f"{ca_folder}/{ca_name}/{cert_name}")

    save_private_key(private_key, f"{ca_folder}/{ca_name}/{cert_name}/{cert_name}.key")
    save_certificate(cert, f"{ca_folder}/{ca_name}/{cert_name}/{cert_name}.pem")
    save_csr(csr, f"{ca_folder}/{ca_name}/{cert_name}/{cert_name}.csr")