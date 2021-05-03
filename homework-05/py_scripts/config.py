import argparse
import json
import os

parser = argparse.ArgumentParser(description="Python script for parsing access.log")
parser.add_argument('--json', action='store_true',
                    help="Write result of parsing in JSON format")
args = parser.parse_args()


def write_result(msg, filename, data, print_keys=False):
    """
    Write script output result in file
    With '--json' in args print result in JSON format

    :param msg: Message printed before result (i.e. which data was collected in result of script)
    :param filename: Name of the file in which write output
    :param data: Result of script work
    :param print_keys: Print or not data dictionary keys in output file
    :return:
    """
    dir_path = os.path.join(repo_root(), 'py_scripts_output')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(os.path.join(dir_path, f'{filename}.txt'), 'w') as f:
        f.write(msg + '\n')
        if args.json is True:
            f.write(json.dumps(str(data)))
        else:
            if isinstance(data, list):
                for i in data:
                    if print_keys:
                        f.write('\n'.join('\t'.join([k, str(i.get(k))]) for k in i.keys()))
                        f.write('\n')
                    else:
                        f.write('\t'.join(str(i.get(k)) for k in i.keys()))
                        f.write('\n')
            else:
                if print_keys:
                    f.write('\n'.join('\t'.join([k, str(data.get(k))]) for k in data.keys()))
                else:
                    f.write('\t'.join(str(data.get(k)) for k in data.keys()))


def repo_root():
    return os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))
