# pdcutils.py
# utilities for other python data collection
import os

# Ugh, no numpy mean and std on weaver, so we will just write the utilities.
def mean(data):
    n = len(data)
    msum = 0
    for element in data:
        msum += element
    return msum/n

def variance(data): # with Bessel's correction
    n = len(data)
    # n must be at least 2
    vsum = 0
    mmean= mean(data)
    for element in data:
        vsum += (element-mmean)**2
    return vsum / (n-1)

def stdev(data):
    return (variance(data)**0.5)

def gaussian_error(data):
    n = len(data)
    if n == 1:
        return data[0]
    return (stdev(data)/((n-1)**0.5)) # not sure if n-1 necessary, but safe

def find_order(n): # returns x such that 10**x <= n < 10**(x+1)
    order = 0
    while(n >= 10):
        order += 1
        n /= 10
    return order

def generate_log_scale_stepped_array(nmin, nmax, nmul):
    return_arr = []
    ncur = nmin
    while(ncur < nmax):
        return_arr.append(int(ncur))
        ncur *= nmul
        stride = 10**(find_order(ncur)-1)
        ncur = (ncur//stride)*stride
    return_arr.append(int(nmax))
    return return_arr

def generate_log_scale_array(nmin, nmax, nmul):
    return_arr = []
    ncur = nmin
    while(ncur < nmax):
        return_arr.append(int(ncur))
        ncur *= nmul
    return_arr.append(int(nmax))
    return return_arr

def generate_run_ns_file(fname, nmin, nmax, nmul, mode="log_stepped"):
    f = open(fname, "w")

    if mode == "log_stepped":
        arr = generate_log_scale_stepped_array(nmin, nmax, nmul)
    else:
        arr = None

    for element in arr:
        f.write(str(element))
        f.write("\n")

    f.close()

def dtype_from_word(dtype, word):
    remove_chars = ['(',')','[',']']
    for target in remove_chars:
        word = word.replace(target,'')
    return dtype(word)

def generate_plot_code(target):
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

def generate_plot_code_dict(target):
    lsitems = os.listdir(target)
    csvs = []
    for item in lsitems:
        if item[-4:] == ".csv":
            csvs.append(item)

    vnames = []
    csvs.sort()
    print("runs = {}")
    for csv in csvs:
        first_ = csv.index('_')
        second_ = csv.index('_', first_+1)
        vname = csv[second_+1:-4]
        vnames.append(vname)
        printstr = ""
        printstr += f"runs[\"{vname}\"] = "
        printstr += "{"
        printstr += f"\"data\" : pd.read_csv(\"{csv}\")"
        printstr += ", "
        printstr += f"\"label\" : \"{vname}\""
        printstr += "}"
        print(printstr)

def count_permutations(src_dict):
    total_permutations = 1
    for key in src_dict:
        total_permutations *= len(src_dict[key]["values"])
    return total_permutations

def get_nth_dict(src_dict, n):
    total_permutations = count_permutations(src_dict)
    new_dict = {}
    for key in src_dict:
        key_arr_len = len(src_dict[key]["values"])
        target = n % key_arr_len
        new_dict[key] = {}
        new_dict[key]["flag"] = src_dict[key]["flag"]
        new_dict[key]["value"] = src_dict[key]["values"][target]
        n = n // key_arr_len
    return new_dict

def get_example_dict():
    ex_dict = {}
    ex_dict["N"] = {}
    ex_dict["TS"] = {}
    ex_dict["N"]["flag"] = "-N"
    ex_dict["TS"]["flag"] = "-TS"
    ex_dict["N"]["values"] = [1,10,500]
    ex_dict["TS"]["values"] = [2,8,16,128]
    return ex_dict
