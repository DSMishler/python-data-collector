class heat3d_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "heat3d_generator"
        self.target_file = "rma/rma_heat3d"
        self.data_dir    = "heat3d_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = "mpirun"
    def generate_params_dict(self, sizes = [1000, 2000], iterations = [1000], NPs = [1]):
        param_dict = {}
        param_dict["size"]={}
        param_dict["size"]["flags"] = ["-X","-Y","-Z"]
        param_dict["size"]["values"] = sizes
        param_dict["iterations"] = {}
        param_dict["iterations"]["flags"] = ["-N"]
        param_dict["iterations"]["values"] = iterations
        param_dict["NPs"] = {}
        param_dict["NPs"]["flags"] = ["-np"]
        param_dict["NPs"]["values"] = NPs
        param_dict["NPs"]["preamble"] = True

        return param_dict
    def set_vals(self, param_dict):
        file_type = self.target_file[:self.target_file.index('/')]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "heat3d_"
        of += f"{file_type}"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
