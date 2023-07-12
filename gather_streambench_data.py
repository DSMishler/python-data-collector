import sys
import os
import socket
import re
import datetime



target_dir   = "~/Kokkos/kokkos-remote-spaces/weaver_build/examples/benchmarks/stream/"
target_file  = "stream_1node"
data_dir     = "streamdata"
hostname     = socket.gethostname()
tmp_fname    = f"mzz_gather_{hostname}.txt"
pdc_root     = "~/Kokkos/python-data-collector/"
pdc_cmd      = f"python {pdc_root}python_data_collector.py"
run_ns_fname = f"mzz_run_ns_{hostname}.txt"
today        = str(datetime.date.today())

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

def generate_run_ns_file(fname, nmin, nmax, nmul):
    f = open(fname, "w")

    log_arr = generate_log_scale_stepped_array(nmin, nmax, nmul)

    for element in log_arr:
        f.write(str(element))
        f.write("\n")

    f.close()

def mode_to_char(mode):
    if(mode == 0):
        return "n"
    if(mode == 1):
        return "r"
    if(mode == 2):
        return "u"
    return None

def bmode_to_style(mode):
    if(mode == -1):
        return "pp"
    else:
        return "pe"

if __name__ == "__main__":
    os.system(f"mkdir -p {data_dir}")

    generate_run_ns_file(run_ns_fname, 1e5, 1e8, 1.2)

    amodes = [0,1,2]
    bmodes = [-1,0,1,2]
    for amode in amodes:
        for bmode in bmodes:
            of = "" #output file
            of += f"{data_dir}/"
            of += f"{today}_"
            of += f"{hostname}_"
            of += "stream_"
            of += "np1_"
            of += f"{bmode_to_style(bmode)}_"
            of += f"{mode_to_char(amode)}"
            of += "p"
            if bmode == -1:
                of += f"{mode_to_char(amode)}"
            else:
                of += f"{mode_to_char(bmode)}"
            of += ".csv"

            run_fname = f"\"{target_dir}{target_file}"
            run_fname += f" -a {amode} -b {bmode}\""

            pdcstr = ""
            pdcstr += pdc_cmd
            pdcstr += " "
            pdcstr += f"rf {run_fname}"
            pdcstr += " "
            pdcstr += f"nf {run_ns_fname}"
            pdcstr += " "
            pdcstr += f"of {of}"
            pdcstr += " "
            pdcstr += f"tf {tmp_fname}"
            print(pdcstr)
            os.system(pdcstr)
            if os.path.isfile(tmp_fname):
                print("detected pdc abort, manager also aborting")
                exit()


