# This file is for my own log to gather total time spent on projects.
# Logs example:
#
# DATE   START END   CAT PROJECT             SESSION                  SUMMARY
# 201114 12:06 12:31 Lei Lunch               Spaghetti                Yum, spaghetti
#
# Output: "Lunch: 0:26"

import argparse
from collections import defaultdict
from datetime import datetime, timedelta

import tbtl_parse


TBTL_LOG = '/Users/oldsilverboi/Dropbox (Personal)/PARA/0 Meta/log.tbtl'


def get_total_time_logged_by_project(entries: list) -> str:
    project_sums = defaultdict(timedelta)
    for entry in entries:
        project = entry["PROJECT"]
        if entry.get('START') is not None:
            start_time = datetime.strptime(entry['START'], "%H:%M")
            end_time = datetime.strptime(entry['END'], "%H:%M")
            if end_time < start_time:
                end_time += timedelta(hours=24)
            time_spent = end_time - start_time
        else:
            hour_time, minute_time = [int(num) for num in entry.get('END').split(':')]
            time_spent = timedelta(hours=hour_time, minutes=minute_time)
        project_sums[project] += time_spent
    output = "\n"
    for project, total_time in project_sums.items():
        output += f"{project}: {total_time}\n"
    return output


if __name__ == "__main__":
    log = tbtl_parse.parse_tablatal_file(TBTL_LOG)
    print(get_total_time_logged_by_project(log))
