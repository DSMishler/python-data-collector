import pdcutils

class teams_benchmark_handler:
    def __init__(self, infodict):
        self.name = "teams benchmark handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_benchmark": [], "gups": []}
    def generate_commandstr(self, n, iterations):
        commandstr = ""
        if (self.infodict['run_preamble']['value'] is not None):
            commandstr += f"{self.infodict['run_preamble']['value']} "
        commandstr += f"{self.infodict['run_fname']['value']} "
        commandstr += f"-N {n} "
        commandstr += f"-I {iterations} "
        commandstr += f"1>{self.infodict['stdout_fname']['value']} "
        commandstr += f"2>{self.infodict['stderr_fname']['value']}"
        return commandstr
    def parse_tmp(self, iterations, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time_benchmark = -1
        gups           = -1

        lines = f.read().split('\n')
        words = lines[0].split(',')
        time_benchmark = pdcutils.dtype_from_word(float, words[4])
        gups           = pdcutils.dtype_from_word(float, words[7])

        data_dest["time_benchmark"].append(time_benchmark)
        data_dest["gups"].append(gups)

        f.close()
