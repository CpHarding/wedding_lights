import asyncio
import json
import logging
import threading
import time

import httpx

import light_scan

logger = logging.getLogger('WeddingLights.lights')
logger.setLevel(logging.DEBUG)

DEFAULT_RESCAN_DELAY = 5 * 60  # seconds


class LightManager:

    def __init__(self, settings=None):
        self.settings = settings if isinstance(settings, dict) else {}
        logger.info('Getting clients...')
        self.clients = self.read_clients()
        logger.info(f'Clients: {self.clients}')
        self.refresh_clients()

    def set_lights(self, msgs, addrs='ALL'):
        """
        Set a range of addrs with msgs
        :param msgs: single, or list of light message states
        :param addrs: single, or list of light addresses
        :return: None
        """
        if addrs == 'ALL':
            addrs = list(self.clients.values())
        asyncio.run(self.lights_async(addrs, msgs))

    def decode_state(self, state):
        """
        Decode a "state" and send it to the lights
        :param state: dict of state
        :return:
        """
        if 'all' in [k.lower() for k in state.keys()]:
            self.set_lights(state['all'])
        else:
            lights = []
            states = []
            for light_num, light_state in state.items():
                if self.clients.get(self.settings['tables'].get(light_num, False)):
                    lights.append(self.clients[self.settings['tables'][light_num]])
                    states.append(light_state)
            logger.debug(f'Lights: {lights}')
            logger.debug(f'States: {states}')
            self.set_lights(states, addrs=lights)

    def read_clients(self, scan=None):
        """
        Find clients
        :param scan: If True, force a network rescan, else use settings value
        :return: Clients
        """
        scan = True if scan else self.settings.get('scan', True)
        try:
            return light_scan.nmap(scan)
        except Exception:
            with open(light_scan.FILENAME) as f:
                contents = json.load(f)
            return contents

    def refresh_clients(self):
        """
        Triggers a client rescan every self.settings['refresh_delay'] seconds
        :return:
        """

        def _refresh():
            while True:
                logger.debug('rescanning for clients')
                self.clients = self.read_clients(False)
                time.sleep(self.settings.get('refresh_delay', DEFAULT_RESCAN_DELAY))

        t = threading.Thread(target=_refresh)
        t.daemon = True
        t.start()

    @staticmethod
    async def lights_async(addrs, msg_dicts):
        """
        Set a range of addrs with msgs
        :param addrs: single, or list of light addresses
        :param msg_dicts: single, or list of light message states
        :return: None
        """
        # Convert to lists if needed
        addrs = addrs if isinstance(addrs, list) else [addrs]
        msgs = msg_dicts if isinstance(msg_dicts, list) else [msg_dicts] * len(addrs)

        async def fetch(addr, msg_string, client):
            logger.info(f'messaging {addr} - {msg_string}')
            try:
                return await client.get(f'http://{addr}/{msg_string}')
            except httpx.HTTPError:
                pass

        # Convert message dict to required string
        strings = []
        for m in msgs:
            ms = f'{m["funct"]}?'
            for k in 'mpscrgb':
                ms += f'&{k}={m.get(k)}' if m.get(k) is not None else ''
            strings.append(ms)
        # Send messages
        async with httpx.AsyncClient() as client:
            responses = await asyncio.gather(*[fetch(a, s, client) for a, s in zip(addrs, strings)])
        # Log responses
        for r in responses:
            try:
                logger.debug(r.text) if r else logger.warning(r.status_code, r.text)
            except AttributeError:
                pass
