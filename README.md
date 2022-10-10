This repository is for training and testing slot filling models from various tasks.
Its goal is to provide you following advantages:
- **Dynamic Keras model creation** by specifying your architecture in config.yaml file. See example/configs for sample configs.
- **Easy to add Pytorch and Tensorflow available models** by providing basics like data generators.
- **Easy model evaluation**.
- **Adding different tasks to train** were never been easy before.

## Creating Environments

**For Keras/Tensorflow models**

If you want to create, train and evaluate Keras/Tensorflow models, create this environment.

```bash
conda env create -f tensorflow_env.yml
```


**For Pytorch models**

If you want to create, train and evaluate Pytorch models, create this environment.

```bash
conda env create -f torch_env.yml
```

## Training and Evaluating Models

sample scripts to train and evaluate models are available in `./scripts` directory.
Just prepare your task, specify your cuda version in `LD_LIBRARY_PATH` and GPUs to use in `CUDA_VISIBLE_DEVICES` in your script and the rest is the same as sample `.sh` files. 
Use command `chmod 750 YourFile.sh` to set required permissions, then execute it. 

## Adding Tasks
To add your task, just inherit Task class and implement required methods to load templates and implement your task util in the same format as BuyCharge and HotelReservation tasks.