class stream_1node_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "stream_1node_generator"
        self.target_file = "stream_1node"
        self.data_dir    = "stream_1node_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = ""
    def mode_to_char(self, mode):
        if(mode == 0):
            return "n"
        if(mode == 1):
            return "r"
        if(mode == 2):
            return "u"
        return None
    def bmode_to_style(self, mode):
        if(mode == -1):
            return "pp"
        else:
            return "pe"
    def generate_param_dict_list(self):
        param_dict_list = []
        amodes = [0,1,2]
        bmodes = [-1,0,1,2]
        for amode in amodes:
            for bmode in bmodes:
                param_dict_list.append({"amode": amode, "bmode": bmode})
        return param_dict_list
    def set_vals(self, param_dict):
        amode = param_dict["amode"]
        bmode = param_dict["bmode"]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "stream_"
        of += "np1_"
        of += f"{self.bmode_to_style(bmode)}_"
        of += f"{self.mode_to_char(amode)}"
        of += "p"
        if bmode == -1:
            of += f"{self.mode_to_char(amode)}"
        else:
            of += f"{self.mode_to_char(bmode)}"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file} -a {amode} -b {bmode}"

        self.out_fname = of
        self.run_fname = rf
