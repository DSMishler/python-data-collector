import pdcutils

class stream_benchmark_handler:
    def __init__(self, infodict):
        self.name = "stream benchmark handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_total" : [], "time_stream": [], "GUPs": [], "bandwidth": []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time = -1
        time_stream = -1
        GUPs = -1
        bandwidth = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            try:
                int(words[0])
            except ValueError:
                continue
            if int(words[0]) == param_dict["iterations"]["value"]:
                for j in range(len(words)):
                    if words[j] == "Time":
                        time = pdcutils.dtype_from_word(float, words[j+1])
                        break
                # next line has stream time
                words = lines[i+1].split()
                for j in range(len(words)):
                    if words[j] == "stream:":
                        time_stream = pdcutils.dtype_from_word(float, words[j+1])
                # following line has GUPs and bandwidth
                words = lines[i+2].split()
                for j in range(len(words)):
                    if words[j] == "GUPs:":
                        GUPs = pdcutils.dtype_from_word(float, words[j+1])
                    if words[j] == "bandwidth:":
                        bandwidth = pdcutils.dtype_from_word(float, words[j+1])

                break
        data_dest["time_total"].append(time)
        data_dest["time_stream"].append(time_stream)
        data_dest["GUPs"].append(GUPs)
        data_dest["bandwidth"].append(bandwidth)

        f.close()
