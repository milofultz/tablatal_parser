import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("--headers", help="write names of column headers, separated by commas", type=str)
args = parser.parse_args()


def create_tbtl_data(data: list, ordered_headers: list) -> str:
    field_lengths = get_field_lengths(data, ordered_headers)
    return format_parsed_data(data, ordered_headers, field_lengths)


def get_field_lengths(data: list, headers: list) -> dict:
    field_data = {field: len(field) for field in headers}
    for entry in data:
        for key, value in entry.items():
            if value is not None and len(str(value)) > field_data[key]:
                field_data[key] = len(str(value))
    return field_data


def format_parsed_data(data: list, headers: list, lengths: dict) -> str:
    entries = []
    header_line = ""
    for header in headers:
        header_line += header.upper().ljust(lengths[header]) + ' '
    entries.append(header_line.strip())
    for entry in data:
        line = ""
        for header in headers:
            if entry[header] is not None:
                line += str(entry[header]).ljust(lengths[header]) + ' '
            else:
                line += ' ' * lengths[header] + ' '
        entries.append(line.strip())
    return '\n'.join(entry for entry in entries)


if __name__ == "__main__":
    with open(args.input, 'r') as f:
        parsed_data = json.load(f)
    ordered_headers = [header.strip() for header in args.headers.split(',')]
    tbtl_data = create_tbtl_data(parsed_data, ordered_headers)
    print(tbtl_data)
