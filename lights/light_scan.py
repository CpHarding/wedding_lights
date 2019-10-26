import json
import logging
import os
import re
import subprocess

import requests

RE_ARP_MAC = re.compile(r'\? \(([0-9]+.[0-9]+.[0-9]+.[0-9]+)\) at ([a-zA-Z0-9:]+)')
RE_NMAP_MAC = re.compile(r'Nmap scan report for ([0-9]+.[0-9]+.[0-9]+.[0-9]+)')

logger = logging.getLogger('light_scan')

FILENAME = 'clients.json'


def nmap(scan=True):
    clients = []
    mc_clients = {}
    if not scan and os.path.isfile(FILENAME):
        with open(FILENAME) as f:
            mc_clients = json.load(f)
    else:
        rsp = subprocess.run('nmap -sn 192.168.1.200-254'.split(), stdout=subprocess.PIPE)
        for line in rsp.stdout.decode('utf-8').split('\n'):
            match = RE_NMAP_MAC.search(line)
            if match:
                clients.append(match.group(1))
        logger.debug(f'Active Clients: {clients}')

        for client in clients:
            try:
                rsp = requests.get(f'http://{client}/esp_status')
                if rsp.status_code != 404:
                    response = rsp.json()
                    mc_clients[response['HOSTNAME']] = client
            except requests.RequestException:
                pass
        logger.info(f'Mclighting Clients: {mc_clients}')

        with open(FILENAME, 'w') as f:
            f.write(json.dumps(mc_clients))

    return mc_clients


if __name__ == '__main__':
    nmap()
