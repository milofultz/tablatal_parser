# This file is for my own log to gather total time spent on projects.
# Logs example:
#
# DATE   START END   CAT PROJECT             SESSION                  SUMMARY
# 201114 12:06 12:31 Lei Lunch               Spaghetti                Yum, spaghetti
#
# Output: "Lunch: 0:26"

import argparse
from datetime import datetime, timedelta

import tbtl_parse


def get_total_time_logged_by_project(entries: list) -> str:
    project_sums = dict()
    for entry in entries:
        project = entry["PROJECT"]
        if entry.get('START') is not None:
            start_time = datetime.strptime(entry['START'], "%H:%M")
            end_time = datetime.strptime(entry['END'], "%H:%M")
            time_spent = end_time - start_time
        else:
            hours_time, minute_time = [int(num) for num in entry.get('END').split(':')]
            time_spent = timedelta(hours=hour_time, minutes=minute_time)
        if projects.get(project_name) is None:
            project_sums[project] = timedelta()
        project_sums[project] += time_spent
    output = "\n"
    for project in project_sums.keys():
        total_hours, remainder = divmod(project_sums[project].seconds, 3600)
        total_minutes = remainder // 60
        output += f"{project}: {total_hours}:{total_minutes:02}\n"
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file to be parsed")
    args = parser.parse_args()

    log = tbtl_parse.parse_tablatal_file(args.input)
    print(get_total_time_logged_by_project(log))
