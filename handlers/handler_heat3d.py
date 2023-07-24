import pdcutils

class heat3d_handler:
    def __init__(self, infodict):
        self.name = "head3d handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time" : [], "compute_time": [], "dt_time": []}
    def generate_commandstr(self, n, N):
        commandstr = ""
        if (self.infodict['run_preamble']['value'] is not None):
            commandstr += f"{self.infodict['run_preamble']['value']} "
        commandstr += f"{self.infodict['run_fname']['value']} "
        commandstr += f"-X {n} "
        commandstr += f"-Y {n} "
        commandstr += f"-Z {n} "
        commandstr += f"1>{self.infodict['stdout_fname']['value']} "
        commandstr += f"2>{self.infodict['stderr_fname']['value']}"
        return commandstr
    def parse_tmp(self, N, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time = -1
        dt_time = -1
        compute_time = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            try:
                int(words[0])
            except ValueError:
                continue
            if int(words[0]) == N:
                for j in range(len(words)):
                    if words[j] == "Time":
                        time = pdcutils.dtype_from_word(float, words[j+1])
                        break
                # next line is the last line
                words = lines[i+1].split()
                for j in range(len(words)):
                    if words[j] == "surface:":
                        dt_time = pdcutils.dtype_from_word(float, words[j+1])
                    if words[j] == "compute:":
                        compute_time = pdcutils.dtype_from_word(float, words[j+1])

                break
        data_dest["time"].append(time)
        data_dest["compute_time"].append(compute_time)
        data_dest["dt_time"].append(dt_time)

        f.close()
