import re
from collections import Counter
import config


def count_requests_with_server_error():
    ip_list = []
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,} .+HTTP.+" 5.. \d+', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            ip_list.append(match.split()[0])
    keys = Counter(ip_list).keys()
    values = Counter(ip_list).values()
    tuple_list = list(zip(keys, values))
    tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    data = []
    for ip, count in tuple_list[:5:]:
        data.append({'ip': ip, 'count': count})

    config.write_result('Top 5 users with the biggest number of requests with server error (5xx)',
                        'count_requests_with_server_error', data)


count_requests_with_server_error()