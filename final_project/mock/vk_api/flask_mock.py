import json
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS = {}  # Dictionary {"username": vk_id}


@app.route('/vk_id/<name>', methods=['GET'])
def get_user_surname(name):
    if vk_id := USERS.get(name):
        return jsonify({'vk_id': vk_id}), 200
    else:
        return jsonify({}), 404


@app.route('/create_vk_id', methods=['POST'])
def create_user_surname():
    user_info = json.loads(request.data)
    USERS.update(user_info)
    return jsonify({}), 202


if __name__ == '__main__':
    host = 'vkapi'
    port = '8088'

    app.run(host, port)



