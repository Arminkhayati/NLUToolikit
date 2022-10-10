#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR
eval "$(conda shell.bash hook)"
conda activate torch4
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-9.0/lib64
export CUDA_VISIBLE_DEVICES="2,3"
python ../main/core/evaluation/conv_seq2seq/on_text.py