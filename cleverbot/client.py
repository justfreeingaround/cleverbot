from collections import deque, namedtuple
from hashlib import md5
from typing import Union
from urllib.parse import quote

import httpx

response_cache = namedtuple('response_cache', ['cbs', 'response', 'xai'], defaults=[None, None, None])

class CleverBotClient():
    
    def __init__(self, session: 'Union[httpx.AsyncClient, httpx.Client]', service_url: str):
        self.history = deque(maxlen=6)
        self.session = session

        self.response_cache = response_cache()
        self.service_url = service_url


    @staticmethod
    def quote(message: 'str'):
        return quote(message).replace('%u', '|')

    def create_payload(self, message: 'str'):
        payload = "stimulus={}&".format(self.quote(message)) + \
         '&'.join('vText{}={}'.format(_, self.quote(ctx_item)) for _, ctx_item in enumerate(list(self.history), 2)) + \
            "&cb_settings_language=en&cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="

        return payload + md5(payload[7:33].encode()).hexdigest()

    def construct_parameters(self, message: 'str', cbs=None, xai=None, last_response=None):
        params = {
            'uc': 'UseOfficialCleverbotAPI',
        }

        if cbs is not None:
            params.update(
                {
                    'out': self.quote(last_response),
                    'in': self.quote(message),
                    'bot': 'c',
                    'cbsid': cbs,
                    'xai': xai,
                    'ns': '3',
                    'al': '',
                    'dl': 'en',
                    'flag': 'B',
                    'user': '',
                    'mode': '1',
                    'alt': '0',
                    'reac': '',
                    'emo': '',
                    'sou': 'website',
                    'xed': '',
                }
            )

        return params

    async def acommunicate(self, message: 'str'):
        return self.register(message, await self.session.post(self.service_url, params=self.construct_parameters(message, *self.response_cache), data=self.create_payload(message)))
        
    def communicate(self, message: 'str'):
        return self.register(message, self.session.post(self.service_url, params=self.construct_parameters(message, *self.response_cache), data=self.create_payload(message)))

    def register(self, message: 'str', http_response: 'httpx.Response'):
        
        if http_response.status_code != 200:
            return None
        
        lines = http_response.text.splitlines()
        response, cbs = lines[:2]

        xai = "{},{}".format(cbs[:3], lines[2])


        self.response_cache = response_cache(
            cbs=cbs,
            response=response,
            xai=xai
        )
        self.history.extendleft((message, response))
        return response

    @classmethod
    async def ainitialise(cls, session: 'httpx.AsyncClient', *, url='https://www.cleverbot.com/', service_endpoint='webservicemin'):
        await session.get(url)
        return cls(session, url + service_endpoint)

    @classmethod
    def initialise(cls, session: 'httpx.Client', *, url='https://www.cleverbot.com/', service_endpoint='webservicemin'):
        session.get(url)
        return cls(session, url + service_endpoint)
