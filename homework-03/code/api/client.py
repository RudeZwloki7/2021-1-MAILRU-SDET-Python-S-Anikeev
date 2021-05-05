import logging
from urllib.parse import urljoin

import requests

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 500
MAX_CAMPAIGNS_SHOW = 200
MAX_SEGMENTS_SHOW = 200


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_token(self, user, password):
        location = 'https://auth-ac.my.com/auth'

        headers = self.post_headers
        headers.update({
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        self.session.request('POST', location, headers=headers, data=data, allow_redirects=False)

    def _request(self, method, location, headers=None, data=None, json=None, params=None, files=None,
                 expected_status=200, jsonify=True):
        url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, expected_status)
        if json is not None:
            response = self.session.request(method, url, headers=headers, json=json)
        else:
            response = self.session.request(method, url, headers=headers, data=data, params=params, files=files)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            return json_response
        return response

    @property
    def post_headers(self):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }

    def post_login(self, user, password):
        location = '/csrf/'

        self.get_token(user, password)
        csrftoken = self._request('GET', location, jsonify=False)

        return csrftoken

    def post_create_campaign(self, name, logo_path):
        location = '/api/v2/campaigns.json'

        headers = self.post_headers
        headers.update({
            'Referer': 'https://target.my.com/campaign/new',
            'X-CSRFToken': self.session.cookies.get('csrftoken')
        })

        url_id = self._request('GET', '/api/v1/urls/', params={'url': 'mail.ru'})['id']
        logo_headers = headers
        logo_headers.pop('Content-Type')  # Correct Content-Type value will be set up automatically
        logo = {'file': ("logo.png", open(logo_path, 'rb'), 'image/png')}
        pic_id = self._request('POST', '/api/v2/content/static.json', headers=logo_headers, files=logo)['id']

        campaign_json = {
            "name": name,
            "objective": "traffic",
            "autobidding_mode": "second_price_mean",
            "mixing": "fastest",
            "package_id": 961,
            "banners": [{
                "urls": {
                    "primary": {
                        "id": url_id
                    }
                },
                "textblocks": {},
                "content": {
                    "image_240x400": {
                        "id": pic_id
                    }
                },
                "name": ""
            }]
        }
        campaign_id = self._request('POST', location, headers=headers, json=campaign_json)['id']
        campaign_list = self._request('GET', location, params={'limit': MAX_CAMPAIGNS_SHOW})['items']

        assert campaign_id in [c['id'] for c in campaign_list]

        deleted_status = {'status': "deleted"}
        self._request('POST', f'/api/v2/campaigns/{campaign_id}.json', headers,
                      json=deleted_status, expected_status=204, jsonify=False)

    def post_create_segment(self, name):
        segment_id = self.create_segment(name)
        segments = self.get_segment_list()

        assert segment_id in [s['id'] for s in segments['items']]
        self.delete_segment_by_id(segment_id)

    def post_delete_segment(self, name):
        segment_id = self.create_segment(name)
        self.delete_segment_by_id(segment_id)
        segments = self.get_segment_list()['items']

        assert segment_id not in [s['id'] for s in segments]

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  f'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def get_segment_list(self):
        location = '/api/v2/remarketing/segments.json'
        return self._request('GET', location, params={'limit': MAX_SEGMENTS_SHOW})

    def delete_segment_by_id(self, segment_id):
        location = f'/api/v2/remarketing/segments/{segment_id}.json'

        headers = self.post_headers
        headers.update({'X-CSRFToken': self.session.cookies.get('csrftoken')})

        self._request('DELETE', location, headers=headers, jsonify=False, expected_status=204)

    def create_segment(self, name):
        location = '/api/v2/remarketing/segments.json'

        headers = self.post_headers
        headers.update({
            "X-CSRFToken": self.session.cookies.get('csrftoken'),
        })

        json = {
            "name": name,
            "pass_condition": 1,
            "relations":
                [{
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }],
            "logicType": "or"
        }

        segment_id = self._request('POST', location, headers=headers, json=json)['id']
        return segment_id
