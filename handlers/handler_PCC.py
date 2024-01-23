import pdcutils

class PCC_handler:
    def __init__(self, infodict):
        self.name = "PCC handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_total" : []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time = -1
        appended_something = False

        lines = f.read().split('\n')
        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] == "time:":
                    time = pdcutils.dtype_from_word(float, words[i+1])
                    break
            if time != -1:
                data_dest["time_total"].append(time)
                appended_something = True


        if appended_something is False:
            data_dest["time_total"].append(-1)

        f.close()
