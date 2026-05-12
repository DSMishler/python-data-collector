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


files_to_read = {category: [] for category in categories}

all_files = os.listdir(timing_dir)
for fname in all_files:
    for category in categories:
        if fname[:len(category)] == category:
            files_to_read[category].append(fname)
            break

timings = {category: [] for category in categories}

for cat in files_to_read:
    category = files_to_read[cat]
    for fname in category:
        f = open(timing_dir+fname, "r")
        val = float(f.read())
        f.close()
        timings[cat].append(val)


attributes = [
    "preprocess",
    "input",
    "output",
    "compute"]

for att in attributes:
    # get the times
    att_begin = None
    att_end = None
    for cat in timings:
        if cat[:len(att)] == att:
            if "begin" == cat[-5:]:
                att_begin = timings[cat]
            elif "end" == cat[-3:]:
                att_end = timings[cat]
            else:
                print(f"error, {cat} is not a beginning or end?")
    true_begin = min(att_begin)
    true_end = max(att_end)
    true_time = true_end-true_begin
    print(f"time_{att}: {true_time}")


print(f"parser end at {datetime.datetime.now()}")
