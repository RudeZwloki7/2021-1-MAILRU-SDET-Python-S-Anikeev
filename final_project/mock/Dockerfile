FROM python:3.8-slim-buster
WORKDIR /vk_api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3","-u","./vk_api/flask_mock.py"]