import logging
from urllib.parse import urljoin

import allure
import requests

from api.str_values import StatusCodes

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 500


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

    status = StatusCodes()

    @allure.step('Send request on {location}')
    def _request(self, method, location, headers=None, data=None, json=None, params=None, files=None,
                 expected_status=status.SUCCESS, jsonify=True):

        url = urljoin(self.base_url, location)

        self.log_pre(method, url, headers, data, json, expected_status)
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
        }

    @allure.step('Send auth request')
    def post_login(self, username, password):
        location = '/login'
        headers = self.post_headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {
            "username": f"{username}",
            "password": f"{password}",
            "submit": "Login"
        }

        self._request('POST', location, headers, data, jsonify=False)

    @allure.step('Add new user')
    def post_add_user(self, username, password, email, exp_status=status.CREATED):
        location = '/api/add_user'
        headers = self.post_headers
        data = {
            "username": f"{username}",
            "password": f"{password}",
            "email": f"{email}"
        }

        self._request('POST', location, headers, json=data, expected_status=exp_status, jsonify=False)

    @allure.step('Delete user')
    def get_delete_user(self, username, exp_status=status.DELETED):
        location = f'/api/del_user/{username}'
        headers = self.post_headers

        self._request('GET', location, headers, expected_status=exp_status, jsonify=False)

    @allure.step('Block user')
    def get_block_user(self, username, exp_status=status.SUCCESS):
        location = f'/api/block_user/{username}'
        headers = self.post_headers

        self._request('GET', location, headers, expected_status=exp_status, jsonify=False)

    @allure.step('Unblock user')
    def get_unblock_user(self, username, exp_status=status.SUCCESS):
        location = f'/api/accept_user/{username}'
        headers = self.post_headers

        self._request('GET', location, headers, expected_status=exp_status, jsonify=False)

    @allure.step('Get app status')
    def get_status(self):
        location = f'/status'
        headers = self.post_headers

        response = self._request('GET', location, headers)
        return response

    @staticmethod
    def log_pre(method, url, headers, data, json, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'JSON: {json}\n\n'
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
