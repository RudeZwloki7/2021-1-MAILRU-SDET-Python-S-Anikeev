import logging
import socket
import json
import settings

logger = logging.getLogger('test')


class HttpClient:
    host = settings.MOCK_HOST
    port = int(settings.MOCK_PORT)

    def _request(self, client, method, params, data=None, jsonify=False):
        request = f'{method} {params} HTTP/1.1\r\n' \
                  'Host:{self.host}\r\n'
        if jsonify:
            data = json.dumps(data)
            length = str(len(data))
            request = request + \
                      f'Content-Type: application/json\r\n' \
                      f'Content-Length: {length}\r\n\r\n' \
                      f'{data}'
        else:
            request = request + '\r\n'

        self.log_request(method, request)

        client.send(request.encode())
        response = self._collect_data(client)

        handled_data = self._handle_response(response)

        self.log_response(handled_data)

        return handled_data

    def _setup_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((self.host, self.port))
        return client

    def _collect_data(self, client):
        total_data = []

        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                client.close()
                break

        data = ''.join(total_data).splitlines()

        return data

    def get_user_surname(self, username):
        client = self._setup_connection()

        params = f'/get_surname/{username}'

        resp = self._request(client, 'GET', params)

        return resp

    def update_user_surname(self, username, surname):
        client = self._setup_connection()

        params = f'/update_surname/{username}'
        data = {username: surname}

        resp = self._request(client, 'PUT', params, data, jsonify=True)

        return resp

    def delete_user_surname(self, username):
        client = self._setup_connection()

        params = f'/delete_surname/{username}'

        resp = self._request(client, 'DELETE', params)

        return resp

    @staticmethod
    def log_request(method, request):
        logger.info(
            f'Performing {method} request:\n'
            f'{request}\n'
        )

    @staticmethod
    def log_response(response_data):
        logger.info(
            f'Got response:\n'
            f'STATUS CODE: {response_data["status_code"]}\n'
            f'HEADERS: {response_data["headers"]}\n'
            f'BODY: {response_data["body"]}\n'
        )

    def _handle_response(self, response):
        data = {}
        data['status_code'] = response[0].split()[1]

        headers = ''
        for s in response:
            if s == '':
                data['headers'] = headers
                break
            else:
                headers = headers + s + '\n'

        body = response[-1]
        data['body'] = json.loads(body) if body != '' else body

        return data
