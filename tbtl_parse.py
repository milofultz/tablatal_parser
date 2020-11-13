"""

In the Tablatal file, the first line declares the key, the spacing between each
key defines the length of the parameters for all subsequent lines.

"""

import argparse
import json
import sys


from utilities import load_data, get_headers_info_from_line


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("output", help="filepath to write parsed data as JSON")
parser.add_argument("--headers",
                    help="define headers of columns, separated by commas",
                    type=str)
args = parser.parse_args()


def parse_tablatal_file(filepath, header_names: list = None) -> list:
    tablatal_data = load_data(filepath)
    tablatal_data = tablatal_data.split('\n')
    output = parse_tablatal_data(tablatal_data, header_names)
    return output


def parse_tablatal_data(tablatal_data: list, header_names: list) -> list:
    headers, entries = get_headers_and_entries(tablatal_data, header_names)
    database = []
    for line in entries:
        if line == '' or line[0] == ';':
            continue
        entry = create_entry(headers, line)
        database.append(entry)
    return database


def get_headers_and_entries(tablatal_data, header_names: list):
    for index, line in enumerate(tablatal_data):
        if line in [';', '']:
            continue
        if line == line.upper():
            headers = get_headers_info_from_line(line, header_names)
            entries = tablatal_data[index+1:]
            return headers, entries

    print('Header not found')
    sys.exit()


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
    if args.headers is not None:
        header_names = [header.strip() for header in args.headers.split(',')]
    else:
        header_names = None
    parsed_data = parse_tablatal_file(args.input, header_names)
    save_json_data(parsed_data, args.output)
