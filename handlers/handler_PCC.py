import pdcutils

class PCC_handler:
    def __init__(self, infodict):
        self.name = "PCC handler"
        self.infodict = infodict
        return
    def refresh_current_runs(self):
        return {
            "problem_size_n": [],
            "problem_size_k": [],
            "time_total": [],
            "time_input": [],
            "time_precompute": [],
            "time_compute_and_output": [],
            "time_compute": [],
            "time_output": []}
    def parse_tmp(self, param_dict, data_dest):
        f = open(self.infodict['stdout_fname']['value'], "r")

        time_total = None
        time_input = None
        time_precompute = None
        time_compute = None
        time_compute_and_output = None
        time_output = None
        problem_size_n = None
        problem_size_k = None

        lines = f.read().split('\n')
        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] == "time_total:":
                    time_total = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "time_input:":
                    time_input = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "time_precompute:":
                    time_precompute = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "time_compute:":
                    time_compute = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "time_compute_and_output:":
                    time_compute_and_output = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "time_output:":
                    time_output = pdcutils.dtype_from_word(float, words[i+1])
                    break
                if words[i] == "size_n:":
                    problem_size_n = pdcutils.dtype_from_word(int, words[i+1])
                    break
                if words[i] == "size_k:":
                    problem_size_k = pdcutils.dtype_from_word(int, words[i+1])
                    break

        if time_total is not None:
            data_dest["time_total"].append(time_total)
        else:
            pass # will cause handler to abort

        if time_input is not None:
            data_dest["time_input"].append(time_input)
        else:
            pass # will cause handler to abort

        if problem_size_n is not None:
            data_dest["problem_size_n"].append(problem_size_n)
        else:
            pass # will cause handler to abort

        if problem_size_k is not None:
            data_dest["problem_size_k"].append(problem_size_k)
        else:
            pass # will cause handler to abort

        if time_precompute is not None:
            data_dest["time_precompute"].append(time_precompute)
        else:
            data_dest["time_precompute"].append(0) # dummy value for now

        if time_compute is not None:
            data_dest["time_compute"].append(time_compute)
        else:
            data_dest["time_compute"].append(0) # dummy value for now

        if time_compute_and_output is not None:
            data_dest["time_compute_and_output"].append(time_compute_and_output)
        else:
            data_dest["time_compute_and_output"].append(0) # dummy value for now

        if time_output is not None:
            data_dest["time_output"].append(time_output)
        else:
            data_dest["time_output"].append(0) # dummy value for now


        f.close()
