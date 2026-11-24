import os

import datetime

print(f"parser begin at {datetime.datetime.now()}")

timing_dir = "split_timing_data/"

# print(os.listdir(timing_dir))


categories = [
    "preprocess_begin",
    "preprocess_end",
    "input_begin",
    "input_end",
    "output_begin",
    "output_end",
    "compute_begin",
    "compute_end"]



all_timings = {}

for cat in categories:
    all_timings[cat] = {}
    fname = "timing_data/"+cat+".txt"
    f = open(fname)
    ftxt = f.read()
    f.close()
    for line in ftxt.split('\n'):
        if len(line) == 0:
            continue
        (info, walltime) = line.split(':')
        all_timings[cat][info] = float(walltime)


attributes = [
    "preprocess",
    "input",
    "output",
    "compute"]

for att in attributes:
    # get the times
    att_begin = None
    att_end = None
    for cat in all_timings:
        if cat[:len(att)] == att:
            if "begin" == cat[-5:]:
                att_begin = all_timings[cat]
            elif "end" == cat[-3:]:
                att_end = all_timings[cat]
            else:
                print(f"error, {cat} is not a beginning or end?")
    true_begin = min(att_begin.values())
    true_end = max(att_end.values())
    true_time = true_end-true_begin
    print(f"time_{att}: {true_time}")


print(f"parser end at {datetime.datetime.now()}")
