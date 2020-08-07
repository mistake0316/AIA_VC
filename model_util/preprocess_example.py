from model_backend import YidarPreprocess
import json
from collections import namedtuple
import shutil
import os

if __name__ == "__main__":
    config = json.load(open("config.json","r"))
    preprocess_config =  config["preprocess_config"]
    print(convert_config)
    argv = namedtuple("argv", preprocess_config.keys())(*preprocess_config.values())
    YidarPreprocess.process_with_config(argv)
    
    npz_src = config["npz_path"]
    npz_trg = preprocess_config["mc_dir"]
    src_files = os.listdir(npz_src)
    print(src_files)
    for file_name in src_files:
        full_file_name = os.path.join(npz_src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, npz_trg)
