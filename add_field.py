import argparse


from utilities import load_data, save_data, get_headers_info_from_line


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file to be parsed")
parser.add_argument("output", help="filepath to write parsed data as JSON")
args = parser.parse_args()


def find_header_line(lines: str) -> str:
    for line in lines.split('\n'):
        if is_header_line(line):
            return line


def is_header_line(line):
    if line == line.upper() and line not in [';', '']:
        return True
    return False


def get_last_field_length(data: str, header_info: list) -> int:
    longest = 0
    for line in data.split('\n'):
        length = len(line)
        if length > longest:
            longest = length
    return longest - header_info[-1]['start']


def get_new_field_info(headers_info):
    new_field = {}
    new_field['name'] = get_new_field_name()
    new_field['length'] = get_new_field_length()
    new_field['index'] = get_new_field_index(headers_info)
    return new_field


def get_new_field_name() -> str:
    while True:
        name = input("New field name: ").upper()
        if ' ' not in name.strip() or name.strip() != '':
            return name


def get_new_field_length() -> int:
    while True:
        length = input("New field length (excluding ending space): ")
        if length.isnumeric():
            return int(length)


def get_new_field_index(headers_info) -> int:
    while True:
        for i, field in enumerate(headers_info):
            print(f"{i}. {field['name']}")
        index = input("New field index (will insert before existing): ")
        if index.isnumeric() and 0 <= int(index) <= len(headers_info):
            return int(index)


def add_new_field_to_headers_info(new_field_info, headers_info) -> list:
    new_headers_info = headers_info
    new_headers_info.insert(new_field_info['index'],
                            {'name': new_field_info['name'],
                             'start': None,
                             'length': new_field_info['length']})
    start_counter = 0
    for index, header in enumerate(new_headers_info):
        new_headers_info[index]['start'] = start_counter
        start_counter += new_headers_info[index]['length']
    return new_headers_info


def insert_new_field_to_data(new_field_info, data):
    output = ""
    field_name = new_field_info['name']
    start = new_field_info['start']
    length = new_field_info['length'] + 1
    for line in data.split('\n'):
        if is_header_line(line):
            output += line[:start] + field_name.ljust(length) + line[start:]
        elif line == '' or line[0] == ';':
            output += line
        else:
            output += line[:start] + (' ' * length) + line[start:]
        output += '\n'
    return output


if __name__ == "__main__":
    tablatal_data = load_data(args.input)
    header_line = find_header_line(tablatal_data)
    headers_info = get_headers_info_from_line(header_line)
    headers_info[-1]['length'] = get_last_field_length(tablatal_data, headers_info)
    new_field_details = get_new_field_info(headers_info)
    new_headers_info = add_new_field_to_headers_info(new_field_details, headers_info)
    new_field_info = new_headers_info[new_field_details['index']]
    tablatal_data = insert_new_field_to_data(new_field_info, tablatal_data)
    save_data(tablatal_data, args.output)
