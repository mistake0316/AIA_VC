import os
from collections import namedtuple
import collections
import collections.abc

import json


base_config = {
    "preprocess_config":{
        "sample_rate":16000,
        "origin_wavpath": "$BASE_PATH/../DATA/temp_data/temp_input",
        "target_wavpath": "$BASE_PATH/../DATA/temp_data/temp_out",
        "mc_dir": "$BASE_PATH/../DATA/temp_data/temp_mc",
        "num_workers": None
    },
    "npz_path":"$BASE_PATH/../DATA/temp_data/npz_files",
    "origin_wav_name": "$BASE_PATH/../DATA/temp_data/temp_input/temp_speaker/temp_speaker_source.wav",
    "split_token" : "@", 
    "speakers" : ["p262@p262",
                  "p272@p272",
                  "p229@p229",
                  "p232@p232",
                  "p292@p292",
                  "p293@p293",
                  "p360@p360",
                  "p361@p361",
                  "p248@p248",
                  "p251@p251",
                  "p777@蔡英文",
                  "@#韓國瑜",
                  "@#馬英九"],
    "speakers_image":{"蔡英文":"$BASE_PATH/images/english.png",
                      "#韓國瑜":"$BASE_PATH/images/fish.gif",
                      "#馬英九":"$BASE_PATH/images/horse.jpeg"},
    "default_image":"$BASE_PATH/images/convict.jpg",
    "convert_config" : {
        "num_speakers" : 11,
        "num_converted_wavs" : 1,
        "resume_iters" : 195000,
        "src_spk" : "temp_speaker",
        "trg_spk" : "p262",
        "train_data_dir":"$BASE_PATH/../DATA/temp_data/temp_mc/",
        "test_data_dir" :"$BASE_PATH/../DATA/temp_data/temp_mc/",
        "wav_dir" : "$BASE_PATH/../DATA/temp_data/temp_out",
        "log_dir" : "./logs",
        "model_save_dir" : "$BASE_PATH/model_util/model_backend/models_with_Tasi",
        "convert_dir" : "$BASE_PATH/model_util/converted"
    }
}


def replace_token_to_pwd(base_DICT, token):
  for k, v in base_DICT.items():
    if isinstance(v, collections.abc.Mapping):
        base_DICT[k] = replace_token_to_pwd(base_DICT.get(k, {}), token)
    elif isinstance(v, str):
        base_DICT[k] = v.replace(token, os.getcwd())
    else:
        pass
  return base_DICT
    

if __name__ == "__main__":
    token = "$BASE_PATH"
    config = replace_token_to_pwd(base_config, token)
    print(config)
    config_path = os.path.join(os.getcwd(), "config.json")
    json.dump(config, open(config_path,'w'), ensure_ascii=False, indent=4)
