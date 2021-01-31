# This file is for my own log to gather total time spent on projects.
# Logs example:
#
# DATE   START END   CAT PROJECT             SESSION                  SUMMARY
# 201114 12:06 12:31 Lei Lunch               Spaghetti                Yum, spaghetti
#
# Output: "Lunch: 0:26"

from collections import defaultdict
from datetime import datetime, timedelta
from operator import itemgetter
import sys

import tbtl_parse
import utilities


TBTL_LOG = '/Users/oldsilverboi/Dropbox (Personal)/PARA/0 Meta/log.tbtl'
DEF_HEADER = 'DATE   START END   CAT PROJECT             SESSION                  SUMMARY'


def get_total_time_logged_by_project(entries: list) -> str:
    entries = sorted(entries, key=itemgetter('PROJECT')) 

    project_sums = dict()
    for entry in entries:
        project, session = entry["PROJECT"], entry["SESSION"]
        if not project_sums.get(project):
            project_sums[project] = defaultdict(timedelta)
        if entry.get('START') is not None:
            start_time = datetime.strptime(entry['START'], "%H:%M")
            end_time = datetime.strptime(entry['END'], "%H:%M")
            if end_time < start_time:
                end_time += timedelta(hours=24)
            time_spent = end_time - start_time
        else:
            hour_time, minute_time = [int(num) for num in entry.get('END').split(':')]
            time_spent = timedelta(hours=hour_time, minutes=minute_time)
        project_sums[project]["total_time"] += time_spent
        project_sums[project][session] += time_spent
    output = "\n"
    for project, data in project_sums.items():
        output += f"{project}: {data.get('total_time')}\n"
        for session, session_time in data.items():
            if session == "total_time":
                continue
            output += f"    {session}: {session_time}\n"
    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TBTL_LOG = sys.argv[1]
        log = utilities.load_data(TBTL_LOG).split('\n')
        log.insert(0, DEF_HEADER)
    else:
        log = utilities.load_data(TBTL_LOG).split('\n')
    parsed_log = tbtl_parse.parse_tablatal_data(log)
    print(get_total_time_logged_by_project(parsed_log))
