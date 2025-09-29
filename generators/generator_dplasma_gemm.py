class dplasma_gemm_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "dplasma_gemm_generator"
        self.target_file = "testing_dgemm"
        self.data_dir    = "dplasma_gemm_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.pre         = ""

        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "dplasma_dgemm"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
    def generate_params_dict(self, Ns = [1000, 2000], NBs = [200], nruns = [3]):
        param_dict = {}
        param_dict["N"]={}
        param_dict["N"]["flags"] = ["-N"]
        param_dict["N"]["values"] = Ns
        param_dict["NB"]={}
        param_dict["NB"]["flags"] = ["-NB"]
        param_dict["NB"]["values"] = NBs
        param_dict["nruns"]={}
        param_dict["nruns"]["flags"] = ["-nruns"]
        param_dict["nruns"]["values"] = nruns

        return param_dict
