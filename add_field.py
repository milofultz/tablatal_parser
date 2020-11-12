"""

options:
    add_field.py input output


"""

import re

from tbtl_parse import get_headers_info_from_line
from utilities import load_data, save_data


def find_header_line(lines: list) -> str:
    # regex for line
    # return that line
    pass


def get_new_field_name() -> str:
    # auto all caps
    pass


def get_new_field_width() -> int:
    # will add one to end
    pass


def get_new_field_index() -> int:
    # which index to insert before
    pass


def add_new_field_to_tablatal_data(field_name, field_width, tablatal_data) -> list:
    pass


if __name__ == "__main__":
    # load tbtl file
    # header_line = find header line
    # get spacing rules
    #     headers = get_headers_info_from_line(header_line)
    # prompt for new field name
    # prompt for field width
    # prompt for field index
    # add new field to tablatal data
    #     insert header.ljust(width) in header line at start of desired field's index
    #     insert ' '*width at start of desired field's index
    # save_data(tbtl_data, args.output)
