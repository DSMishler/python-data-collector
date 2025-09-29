import pdcutils

class dplasma_syrk_handler:
    def __init__(self, infodict):
        self.name = "dplasma syrk handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_total" : [], "GFLOPs": []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time = -1
        GFLOPs = -1
        appended_something = False

        lines = f.read().split('\n')
        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] == "gflops":
                    GFLOPs = pdcutils.dtype_from_word(float, words[i-1])
                    # will grab the second GFLOPs
                if words[i] == "TIME(s)":
                    time = pdcutils.dtype_from_word(float, words[i+1])
            # print("PDC HANDLER:", time, GFLOPs)
            if time != -1 and GFLOPs != -1:
                data_dest["time_total"].append(time)
                data_dest["GFLOPs"].append(GFLOPs)
                appended_something = True
                time = -1
                GFLOPs = -1


        if appended_something is False:
            assert 0, "error! failed to find something at all"
            data_dest["time_total"].append(-1)
            data_dest["GFLOPs"].append(-1)


        f.close()
