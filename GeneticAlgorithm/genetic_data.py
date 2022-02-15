import json, os


CURR_DIR = os.path.dirname(__file__)
genetic_data_json = f'{CURR_DIR}/gdata.json'


def write_json(data, full):
    with open(full, 'w') as fp:
        json.dump(data, fp, indent=2)


def read_json(full):
    data = None
    with open(full, 'r') as fp:
        data = json.load(fp)
    return data


def read_genetic_data():
    """
    This reads data from disk
    Modify this function to read from:
    Cache, Blob etc
    """
    return read_json(genetic_data_json)


def write_genetic_data(gdata):
    """
    This writes data to disk
    Modify this function to write to:
    Cache, Blob etc
    """
    write_json(gdata, genetic_data_json)
