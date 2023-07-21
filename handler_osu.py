import pdcutils

class osu_benchmark_handler:
    def __init__(self, infodict):
        self.name = "osu benchmark handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_benchmark": [], "time_latency": [], "message_rate": []}
    def generate_commandstr(self, n, iterations):
        commandstr = ""
        if (self.infodict['run_preamble']['value'] is not None):
            commandstr += f"{self.infodict['run_preamble']['value']} "
        commandstr += f"{self.infodict['run_fname']['value']} "
        commandstr += f"-l {n} "
        commandstr += f"-i {iterations} "
        commandstr += f"1>{self.infodict['tmp_fname']['value']} "
        commandstr += f"2>{self.infodict['stderr_fname']['value']}"
        return commandstr
    def parse_tmp(self, iterations, data_dest):
        f = open(self.infodict['tmp_fname']['value'], "r")

        time_benchmark = -1
        time_latency   = -1
        message_rate   = -1
        message_bytes  = -1
        dtype_bytes    = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            if words[0] == "iteration":
                continue

            for j in range(len(words)):
                if words[j] == "dtype_bytes":
                    dtype_bytes = pdcutils.dtype_from_word(int, words[j+1])
                if words[j] == "message_bytes":
                    message_bytes = pdcutils.dtype_from_word(int, words[j+1])
                if words[j] == "latency:":
                    time_latency = pdcutils.dtype_from_word(float, words[j+1])
                if words[j] == "time:":
                    time_benchmark = pdcutils.dtype_from_word(float, words[j+1])
                if words[j] == "rate:":
                    message_rate = pdcutils.dtype_from_word(float, words[j+1])

        data_dest["time_benchmark"].append(time_benchmark)
        data_dest["time_latency"].append(time_latency)
        data_dest["message_rate"].append(message_rate)

        f.close()
