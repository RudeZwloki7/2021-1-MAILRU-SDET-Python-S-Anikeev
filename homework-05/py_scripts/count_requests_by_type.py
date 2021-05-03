import re
import config


def count_requests_by_type():
    dict_counts = {}
    regex = re.compile(r'[A-Z]{3,} .+HTTP', re.MULTILINE)

    with open(config.repo_root() +'/access.log', 'r') as f:
        f = f.read()
        matches = re.findall(regex, f)
        for match in matches:
            type = match.split()[0]
            dict_counts.update({f'{type}': 0})
        for match in matches:
            type = match.split()[0]
            dict_counts[f'{type}'] += 1

    config.write_result('Count all requests by type of request', 'count_requests_by_type', dict_counts, print_keys=True)

count_requests_by_type()
