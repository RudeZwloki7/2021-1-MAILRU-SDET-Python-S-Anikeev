import re
from collections import Counter
import config


def most_frequent_requests():
    request_list = []
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            request_list.append(match.split()[1])
    request_list.sort()
    keys = Counter(request_list).keys()
    values = Counter(request_list).values()
    tuple_list = list(zip(keys, values))
    tuple_list.sort(key=lambda tup: tup[1], reverse=True)
    data = []
    for url, count in tuple_list[:10:]:
        data.append({'url': url, 'count': count})

    config.write_result('Top 10 most frequent requests ', 'most_frequent_requests', data)


most_frequent_requests()
