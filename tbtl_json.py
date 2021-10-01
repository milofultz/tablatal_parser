import argparse
import json
import re
import sys


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("--headers", help="define headers of columns, separated by commas", type=str)
args = parser.parse_args()


def parse_tablatal_data(tablatal_data: list, header_names: list = None) -> list:
    """ Convert tablatal data into list of dicts """
    headers, entries = get_headers_and_entries(tablatal_data, header_names)
    database = []
    for line in entries:
        if line == '' or line[0] == ';':
            continue
        entry = create_entry(headers, line)
        database.append(entry)
    return database


def get_headers_and_entries(tablatal_data: list, header_names: list):
    """ Return headers and entries from data """
    for index, line in enumerate(tablatal_data):
        if line in [';', '']:
            continue
        if line == line.upper():
            headers = get_headers_info_from_line(line, header_names)
            entries = tablatal_data[index+1:]
            return headers, entries

    sys.exit('Header not found. Please use `--headers` flag.')


def get_headers_info_from_line(line: str, header_names: list = None) -> list:
    fields = re.finditer(r'\w+\s*', line)

    headers = []
    if line[0] in [';', ' ']:
        headers.append({'name': ('ID'
                                 if header_names is None
                                 else header_names[0]),
                        'start': 0,
                        'length': re.search('\s+', line).end()})

    for i, field in enumerate(fields):
        field_name = field.group()
        headers.append({'name': (field_name.strip()
                                 if header_names is None
                                 else header_names[i+1]),
                        'start': field.start(),
                        'length': len(field_name)})

    headers[-1]['length'] = None
    return headers


def create_entry(headers: list, line: str) -> dict:
    """ Return entry from the line and headers """
    entry = {}
    for header in headers:
        field_name = header['name']
        entry[field_name] = get_value_from_line(line, header)
    return entry


def get_value_from_line(line: str, field_info: dict):
    """ Return the field value from the line """
    field_start = field_info['start']
    field_length = field_info['length']
    value = line[field_start:]
    value = value[:field_length]
    value = value.rstrip()
    if value == '':
        return None
    else:
        return value


if __name__ == '__main__':
    if args.headers is not None:
        header_names = [header.strip() for header in args.headers.split(',')]
    else:
        header_names = None

    with open(args.input, 'r') as f:
        tablatal_entries = f.read().split('\n')

    parsed_data = parse_tablatal_data(tablatal_entries, header_names)

    print(json.dumps(parsed_data))
