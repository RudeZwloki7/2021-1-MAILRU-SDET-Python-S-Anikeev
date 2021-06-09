import json
import logging

import allure
import requests

logger = logging.getLogger('test')


class VkApiClient:
    def create_vk_id(self, username, vk_id):
        data = json.dumps({username: vk_id})
        response = requests.post('http://vkapi:8088/create_vk_id', data=data)
        logger.debug(f'Setup vk_id {vk_id} for user {username}')
        assert response.status_code == 201

    @allure.step("Get vk_id")
    def get_vk_id(self, username):
        response = requests.get(f'http://vkapi:8088/vk_id/{username}')
        logger.info(f'Get vk_id for user {username}')
        return response
