import numpy as np
import librosa
from .model_backend import YidarConvert, YidarPreprocess
import json
from collections import namedtuple
import collections
import shutil
import os
import sys


debug = True
_print = lambda *args, **kwargs: print(*args, **kwargs) if debug else None


def update(base, to_add):
  for k, v in to_add.items():
    if isinstance(v, collections.abc.Mapping):
        base[k] = update(base.get(k, {}), v)
    else:
        base[k] = v
  return base

def copy_npz_file(src_path, trg_path):
  src_files = os.listdir(src_path)
  _print(src_files)
  for file_name in src_files:
      full_file_name = os.path.join(src_path, file_name)
      if os.path.isfile(full_file_name):
          shutil.copy(full_file_name, trg_path)
  
  

def process_one_sound(signal : np.array, sr:int, config:dict, additional_config=None) -> np.array:
  # config = json.load(open(config_path,'r'))
  if additional_config:
    update(config, additional_config)
    
  preprocess_config =  config["preprocess_config"]
  convert_config = config["convert_config"]

  argv_preprocess = namedtuple("argv_preprocess", preprocess_config.keys())(*preprocess_config.values())
  argv_convert = namedtuple("argv_convert", convert_config.keys())(*convert_config.values())
  
  librosa.output.write_wav(config["origin_wav_name"], signal, sr)

  # =================================================================
  YidarPreprocess.process_with_config(argv_preprocess)
  copy_npz_file( src_path = config["npz_path"],
                 trg_path = preprocess_config["mc_dir"])
  processed_path = YidarConvert.test_Yidar(argv_convert)
  file_path = processed_path[-1]
  
  return librosa.core.load(file_path)
  
 


if __name__ == "__main__":
  path = "/mnt/26EAD496EAD46419/VC/DATA/temp_data/temp_input/temp_speaker/temp_speaker_source.wav"
  signal, sr = librosa.core.load(path)
  print("HI")
  additional_config = {"convert_config":{"trg_spk":"p272"}}
  process_one_sound(signal, sr,config=json.load(open('./config.json','r')), additional_config=additional_config)
