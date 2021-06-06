import json
import requests

data = json.dumps({"test_user": 213123})
requests.post('http://0.0.0.0:8088/create_vk_id', data=data)
