import asyncio
import json
import logging
import threading
import time

import httpx

import light_patterns as lp
import light_scan
import log_ext

logger = log_ext.setup_logger('lights')
logger.setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('httpx').setLevel(logging.INFO)
logging.getLogger('asyncio').setLevel(logging.INFO)


async def lights_async(addrs, msg_dicts):
    async def fetch(addr, msg_string, client):
        logger.info(f'messaging {addr} - {msg_string}')
        try:
            return await client.get(f'http://{addr}/{msg_string}')
        except httpx.HTTPError:
            pass

    # Convert to lists if needed
    addrs = addrs if isinstance(addrs, list) else [addrs]
    msgs = msg_dicts if isinstance(msg_dicts, list) else [msg_dicts] * len(addrs)

    strings = []
    for m in msgs:
        ms = f'{m["funct"]}?'
        for k in 'mpscrgb':
            ms += f'&{k}={m.get(k)}' if m.get(k) is not None else ''
        strings.append(ms)
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[fetch(a, s, client) for a, s in zip(addrs, strings)])

    for r in responses:
        if r:
            logger.debug(r.text)
        else:
            if isinstance(r, httpx.HTTPError):
                logger.warning(r.status_code, r.text)


class LightManager:

    def __init__(self):
        logger.info('Scanning for clients')
        self.clients = self.read_clients()
        logger.info(f'Clients: {self.clients}')

    def all_lights(self, msgs):
        self.set_lights(list(self.clients.values()), msgs)

    def set_lights(self, addrs, msgs):
        asyncio.run(lights_async(addrs, msgs))

    @staticmethod
    def read_clients():
        try:
            return light_scan.nmap()
        except Exception:
            with open('clients.json') as f:
                contents = json.load(f)
            return contents

    def refresh_clients(self):
        def _refresh():
            while True:
                self.clients = self.read_clients()
                time.sleep(60)

        t = threading.Thread(target=_refresh)
        t.daemon = True
        t.start()


if __name__ == '__main__':
    DELAY = 0.5
    lm = LightManager()

    # Cycle all lights through the same mode
    order = [lp.OFF, lp.RED, lp.GREEN, lp.BLUE, lp.RAINBOW, lp.RAINBOW_CYCLE]
    for m in order:
        lm.all_lights(m)
        time.sleep(DELAY)

    # All off
    lm.all_lights(lp.OFF)
    time.sleep(DELAY)

    # Cycle all lights through separate modes
    order = [lp.RED, lp.GREEN, lp.BLUE]
    for i in range(len(order)):
        order.append(order.pop(0))
        lm.all_lights(order)
        time.sleep(DELAY)

    # All off
    lm.all_lights(lp.OFF)
    time.sleep(DELAY)

    # Set lights individually
    lm.set_lights(lm.clients['WeddingLight03'], lp.GREEN)
    time.sleep(DELAY)
    lm.set_lights(lm.clients['WeddingLight04'], lp.BLUE)
    time.sleep(DELAY)
    lm.set_lights(lm.clients['WeddingLight06'], lp.RED)

    # All off
    lm.all_lights(lp.OFF)
    time.sleep(DELAY)