import pdcutils

class teams_benchmark_handler:
    def __init__(self, infodict):
        self.name = "teams benchmark handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_benchmark": [], "gups": [], "bandwidth": []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time_benchmark = -1
        gups           = -1
        bandwidth      = -1

        lines = f.read().split('\n')
        words = lines[0].split(',')
        time_benchmark = pdcutils.dtype_from_word(float, words[4])
        gups           = pdcutils.dtype_from_word(float, words[7])
        bandwidth      = pdcutils.dtype_from_word(float, words[8])

        data_dest["time_benchmark"].append(time_benchmark)
        data_dest["gups"].append(gups)
        data_dest["bandwidth"].append(bandwidth)

        f.close()
