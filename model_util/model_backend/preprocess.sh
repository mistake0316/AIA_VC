#!/bin/bash
python preprocess.py --sample_rate 16000 \
                    --origin_wavpath /mnt/26EAD496EAD46419/VC/DATA/VCTK-Corpus/wav48 \
                    --target_wavpath /mnt/26EAD496EAD46419/VC/DATA/VCTK-Corpus/wav16 \
                    --mc_dir_train data/mc/train \
                    --mc_dir_test data/mc/test
