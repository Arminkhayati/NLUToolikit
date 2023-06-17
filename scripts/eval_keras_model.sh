
#!/usr/bin/env bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $DIR
eval "$(conda shell.bash hook)"
conda activate tensorflow
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.2/lib64
export CUDA_VISIBLE_DEVICES=""
python ../main/core/evaluation/keras_model/interactive.py  -m  ../output/model/RNNEncoder/AccountBalanceTask/full_model.h5  -xt ../output/data_dump/RNNEncoder/AccountBalanceTask/x_tokenizer.pickle  -yt ../output/data_dump/RNNEncoder/AccountBalanceTask/y_tokenizer.pickle
