import json

import requests


class VkApiClient:
    def create_vk_id(self, username, vk_id):
        data = json.dumps({username: vk_id})
        response = requests.post('http://vkapi:8088/create_vk_id', data=data)

        assert response.status_code == 201

    def get_vk_id(self, username):
        response = requests.get(f'http://vkapi:8088/vk_id/{username}')
        return response
