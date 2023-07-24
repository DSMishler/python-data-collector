class teams_bench_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "teams_bench_generator"
        self.target_file = "teams"
        self.data_dir    = "teams_bench_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = ""
    def mode_to_label(self, mode):
        if(mode == 0):
            return "nview"
        if(mode == 1):
            return "rview"
        if(mode == 2):
            return "uview"
        return None
    def generate_param_dict_list(self):
        param_dict_list = []
        modes = [0,1,2]
        team_sizes = [2,4,8,16,32,64,128]
        league_sizes = [2,4,8,16,32,64,128]
        for mode in modes:
            for ts in team_sizes:
                for ls in league_sizes:
                    param_dict_list.append({"mode": mode, "ts": ts, "ls": ls})
        return param_dict_list
    def set_vals(self, param_dict):
        mode = param_dict["mode"]
        ts = param_dict["ts"]
        ls = param_dict["ls"]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "teams_bench_"
        of += "np1_"
        of += f"{self.mode_to_label(mode)}_"
        of += f"TS{ts}_"
        of += f"LS{ls}"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file} -m {mode} -TS {ts} -LS {ls}"

        self.out_fname = of
        self.run_fname = rf
