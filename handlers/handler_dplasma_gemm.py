import pdcutils

class dplasma_gemm_handler:
    def __init__(self, infodict):
        self.name = "dplasma gemm handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {"time_total" : [], "GFLOPs": []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time = -1
        GFLOPs = -1

        lines = f.read().split('\n')
        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] == "gflops":
                    GFLOPs = pdcutils.dtype_from_word(float, words[i-1])
                    break

        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] == "TIME(s)":
                    time = pdcutils.dtype_from_word(float, words[i+1])
                    break



        data_dest["time_total"].append(time)
        data_dest["GFLOPs"].append(GFLOPs)

        f.close()
