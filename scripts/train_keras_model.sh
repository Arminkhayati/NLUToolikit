#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR
eval "$(conda shell.bash hook)"
conda activate tensorflow
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.2/lib64
export CUDA_VISIBLE_DEVICES="0"
python ../main/train.py  -c "../configs/BalanceConfig.yaml"