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
To add your task, 
- Put your dataset templates files in ./data dir. 
- Create a package for it in ./main/tasks/ package.
- Create a YourTask class and inherit Task class. Implement required methods to load templates.
- Implement your task util in the same format as BuyCharge and HotelReservation tasks.
  - **SLOT**: is a dictionary that maps slots in templates to the generator functions for them.
  - **WORD_FILLER**: is a dictionary that maps placeholders in templates to the generator functions for them.
  - **ALL_WORDS**: is a list of all words used in your generators and available words in your dataset.
- Don't forget to also add your task in tasks/loader.py module functions.

## Models
Currently only three type of models are available:
- **RNNEncoder**
- **TransformerEncoder**
- **ConvSeq2Seq** from Convolutional Sequence to Sequence model paper.

## Configs parameters
- name: name of your model. (RNNEncoder, TransformerEncoder, ConvSeq2Seq)
- task: name of your task. (BuyChargeTask, HotelReservationTask)
- seed
- model: your model architecture stays here.
- model_params: your model training parameters stays here.
- data.labels: all labels we are predicitng. 
  Note: `PAD` label and `O` "not slot" label must be 0 and 1 respectively, and `<sos>` and `<eos>` labels are also must be in the list, even if we are not using them.

see one of sample config files for more comments.

