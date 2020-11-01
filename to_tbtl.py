import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("output", help="filepath to write parsed data as JSON")
args = parser.parse_args()


def parse_json_file(filepath) -> list:
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


def create_tbtl_data(data: list) -> str:
    headers = get_headers(data[0])
    ordered_headers = get_header_order(headers)
    field_lengths = get_field_lengths(data, ordered_headers)
    return format_parsed_data(data, ordered_headers, field_lengths)


def get_headers(entry: dict) -> list:
    return [field for field in entry]


def get_header_order(headers: list) -> list:
    ordered_headers = []
    while len(headers) > 0:
        try:
            print("Which field do you want next?\n")
            print('\n'.join(f'{i}. {header}' for i, header in enumerate(headers)))
            index = int(input('► '))
            ordered_headers.append(headers.pop(index))
            print()
        except ValueError:
            print("Please enter the index number\n")
        except IndexError:
            print("Please choose a valid index number\n")
    return ordered_headers


def get_field_lengths(data: list, headers: list) -> dict:
    field_data = {field: len(field) for field in headers}
    for entry in data:
        for key, value in entry.items():
            if value is not None and len(value) > field_data[key]:
                field_data[key] = len(value)
    return field_data


def format_parsed_data(data: list, headers: list, lengths: dict) -> str:
    entries = []
    header_line = ""
    for header in headers:
        header_line += header.ljust(lengths[header]) + ' '
    entries.append(header_line)
    for entry in data:
        line = ""
        for header in headers:
            line += (entry[header].ljust(lengths[header]) + ' '
                     if entry[header] is not None
                     else ' ' * lengths[header] + ' ')
        entries.append(line.strip())
    return '\n'.join(entry for entry in entries)


def save_data(tbtl_data, filepath):
    with open(filepath, 'w') as f:
        f.write(tbtl_data)


if __name__ == "__main__":
    parsed_data = parse_json_file(args.input)
    tbtl_data = create_tbtl_data(parsed_data)
    save_data(tbtl_data, args.output)
