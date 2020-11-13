import re


def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def save_data(data, filepath):
    with open(filepath, 'w') as f:
        f.write(data)


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
