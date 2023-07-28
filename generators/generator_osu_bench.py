class osu_bench_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "osu_bench_generator"
        self.target_file = "osu_bench"
        self.data_dir    = "osu_bench_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = "mpirun -np 2"
    def generate_params_dict(self, lens = [1000, 2000], modes = [4, 5], iters = [5]):
        param_dict = {}
        param_dict["len"]={}
        param_dict["len"]["flags"] = ["-l"]
        param_dict["len"]["values"] = lens
        param_dict["mode"]={}
        param_dict["mode"]["flags"] = ["-m"]
        param_dict["mode"]["values"] = modes
        param_dict["iterations"]={}
        param_dict["iterations"]["flags"] = ["-i"]
        param_dict["iterations"]["values"] = iters

        return param_dict
    def set_vals(self, param_dict):
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "osu_bench_"
        of += "np2"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
