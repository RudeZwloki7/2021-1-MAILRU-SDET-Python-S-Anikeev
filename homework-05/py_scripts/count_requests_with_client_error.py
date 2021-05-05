import re
import config


def count_requests_with_client_error():
    request_list = []
    regex = re.compile(r'\d+\.\d+\.\d+\..+[A-Z]{3,} .+HTTP.+" 4.. \d+', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            request_list.append({'url': match.split()[6],
                                 'status_code': match.split()[8],
                                 'size': int(match.split()[9]),
                                 'ip': match.split()[0]})
    request_list.sort(key=lambda d: d['size'], reverse=True)
    data = []
    for i in range(5):
        data.append(request_list[i])

    config.write_result('Top 5 requests with the biggest weight with client error (4xx)',
                        'count_requests_with_client_error', data)

count_requests_with_client_error()
