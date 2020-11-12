def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def save_data(data, filepath):
    with open(filepath, 'w') as f:
        f.write(data)