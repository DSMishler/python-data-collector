# PCC: Pearson Correlation Coefficient

w_python = "python"

class PCC_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "PCC_generator"
        self.target_file = "PCC_performance_manager.py"
        self.data_dir    = "PCC_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.pre         = ""

        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "PCC"
        of += ".csv"

        rf= f"{w_python} {self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
    def generate_params_dict(self, Ns = [1000, 2001, 10000], ks = [100, 201, 100], codes = ["cpp"], data = ["synthetic"]):
        param_dict = {}
        param_dict["N"]={}
        param_dict["N"]["flags"] = ["-N"]
        param_dict["N"]["values"] = Ns
        param_dict["k"]={}
        param_dict["k"]["flags"] = ["-k"]
        param_dict["k"]["values"] = ks
        param_dict["codes"]={}
        param_dict["codes"]["flags"] = ["-code"]
        param_dict["codes"]["values"] = codes
        param_dict["data"]={}
        param_dict["data"]["flags"] = ["-data"]
        param_dict["data"]["values"] = data

        return param_dict
