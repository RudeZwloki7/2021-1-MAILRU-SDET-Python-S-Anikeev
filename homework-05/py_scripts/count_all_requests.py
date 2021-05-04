import re
import config


def count_all_requests():
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)
    count = 0

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        lines = re.findall(regex, f)
        for match in lines:
            count += 1

    data = dict({'count': count})

    config.write_result('Count of all requests', 'count_all_requests', data)


count_all_requests()
