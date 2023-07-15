import sys
import os
import socket
import re

hostname  = socket.gethostname()

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        target = sys.argv[1]
    else:
        target = "."
    lsitems = os.listdir(target)
    csvs = []
    for item in lsitems:
        if item[-4:] == ".csv":
            csvs.append(item)

    vnames = []
    csvs.sort()
    for csv in csvs:
        first_ = csv.index('_')
        second_ = csv.index('_', first_+1)
        vname = csv[second_+1:-4]
        vnames.append(vname)
        printstr = ""
        printstr += f"{vname} = pd.read_csv"
        printstr += f"(\"{csv}\")"
        print(printstr)

    print(f"dfs = {vnames}".replace("'",""))
    print(f"labels = {vnames}".replace("'", "\""))

