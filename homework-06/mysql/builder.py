import re
from collections import Counter
from conftest import repo_root
from mysql.models import *


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_all_requests(self):
        regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)
        count = 0

        with open(repo_root() + '/access.log', 'r') as f:
            f = f.read()
            lines = re.findall(regex, f)
            for _ in lines:
                count += 1

        all_requests = AllRequests(count=count)
        self.client.session.add(all_requests)
        return all_requests

    def create_requests_by_type(self):
        dict_counts = {}
        requests_list = []
        regex = re.compile(r'([A-Z]{3,}) .+HTTP', re.MULTILINE)

        with open(repo_root() + '/access.log', 'r') as f:
            f = f.read()
            matches = re.findall(regex, f)
            for match in matches:
                dict_counts.update({f'{match}': 0})
            for match in matches:
                dict_counts[f'{match}'] += 1

        for type in dict_counts.keys():
            req_by_type = RequestsByType(type=type, count=dict_counts.get(type))
            self.client.session.add(req_by_type)
            requests_list.append(req_by_type)

        return requests_list

    def create_most_frequent_requests(self):
        request_list = []
        regex = re.compile(r'[A-Z]{3,} (.+) HTTP', re.MULTILINE)

        with open(repo_root() + '/access.log', 'r') as f:
            f = f.read()
            matches = re.findall(regex, f)
            for match in matches:
                request_list.append(match)

        request_list.sort()
        keys = Counter(request_list).keys()
        values = Counter(request_list).values()
        tuple_list = list(zip(keys, values))
        tuple_list.sort(key=lambda tup: tup[1], reverse=True)
        request_list.clear()
        for url, count in tuple_list[:10:]:
            most_frequent_request = MostFrequentRequests(url=url, count=count)
            self.client.session.add(most_frequent_request)
            request_list.append(most_frequent_request)

        return request_list

    def create_client_err_requests(self):
        request_list = []
        regex = re.compile(r'(\d+\.\d+\.\d+\.\d+).+[A-Z]{3,} (.+) HTTP.+" (4..) (\d+)', re.MULTILINE)

        with open(repo_root() + '/access.log', 'r') as f:
            f = f.read()
            matches = re.findall(regex, f)
            for match in matches:
                request_list.append({'url': match[1],
                                     'status_code': match[2],
                                     'size': int(match[3]),
                                     'ip': match[0]
                                     }
                                    )
        request_list.sort(key=lambda d: d['size'], reverse=True)
        data = []
        for i in request_list[:5:]:
            client_err_req = ClientErrRequests(url=i['url'], status_code=i['status_code'], size=i['size'], ip=i['ip'])
            self.client.session.add(client_err_req)
            data.append(client_err_req)

        return data

    def create_server_err_requests(self):
        ip_list = []
        regex = re.compile(r'(\d+\.\d+\.\d+\.\d+).+[A-Z]{3,} (.+) HTTP.+" (5..) (\d+)', re.MULTILINE)

        with open(repo_root() + '/access.log', 'r') as f:
            f = f.read()
            matches = re.findall(regex, f)
            for match in matches:
                ip_list.append(match[0])

        keys = Counter(ip_list).keys()
        values = Counter(ip_list).values()
        tuple_list = list(zip(keys, values))
        tuple_list.sort(key=lambda tup: tup[1], reverse=True)
        request_list = []
        for ip, count in tuple_list[:5:]:
            server_err_req = ServerErrRequests(ip=ip, count=count)
            self.client.session.add(server_err_req)
            request_list.append(server_err_req)

        return request_list
