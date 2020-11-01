"""

In the Tablatal file, the first line declares the key, the spacing between each
key defines the length of the parameters for all subsequent lines.

"""

import argparse
import json
import re
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("output", help="filepath to write parsed data as JSON")
parser.add_argument("--headers", help="define headers of columns, separated by commas", type=str)
args = parser.parse_args()


def parse_tablatal_file(filepath, header_names: list = None) -> list:
    tablatal_data = load_data(filepath)
    tablatal_data = tablatal_data.split('\n')
    output = parse_tablatal_data(tablatal_data, header_names)
    return output


def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def parse_tablatal_data(tablatal_data: list, header_names: list) -> list:
    headers, entries = get_headers_and_entries(tablatal_data, header_names)
    database = []
    for line in tablatal_data:
        if line == '' or line[0] == ';':
            continue
        entry = create_entry(headers, line)
        database.append(entry)
    return database


def get_headers_and_entries(tablatal_data, header_names: list):
    for index, line in enumerate(tablatal_data):
        if line == '':
            continue
        if line == line.upper():
            headers = get_headers_info_from_line(line, header_names)
            entries = tablatal_data[index+1:]
            return headers, entries

    print('Header not found')
    sys.exit()


def get_headers_info_from_line(line: str, header_names: list = None) -> list:
    fields = re.finditer(r'\w+\s*', line)

    headers = []
    if line[0] in [';', ' ']:
        headers.append({'name': ('x'
                                 if header_names is None
                                 else header_names[0]),
                        'start': 0,
                        'length': re.search('\s+', line).end()})

    for i, field in enumerate(fields):
        field_name = field.group()
        headers.append({'name': (field_name.lower().strip()
                                 if header_names is None
                                 else header_names[i+1]),
                        'start': field.start(),
                        'length': len(field_name)})

    headers[-1]['length'] = None
    return headers


def create_entry(headers: list, line: str) -> dict:
    entry = {}
    for header in headers:
        field_name = header['name']
        entry[field_name] = get_value_from_line(line, header)
    return entry


def get_value_from_line(line: str, header_info: dict):
    field_start = header_info['start']
    field_length = header_info['length']
    value = line[field_start:]
    value = value[:field_length]
    value = value.rstrip()
    if value == '':
        return None
    else:
        return value


def save_json_data(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
    header_names = [header.strip() for header in args.headers.split(',')]
    parsed_data = parse_tablatal_file(args.input, header_names)
    save_json_data(parsed_data, args.output)
