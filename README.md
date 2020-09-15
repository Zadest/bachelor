# bachelor
github repo for my bachelor's project

### 0. Setting up the development environment
##### 0.1 Conda

In order to use a virtual environment for the development in Visual Studio, I needed to create one, with the anaconda environment as base.

```bash
conda update -n base -c defaults conda
conda create --name vsBachelor python=3.7 anaconda
conda activate vsBachelor
pip install tensorflow
pip install keras
conda install -c anaconda pillow
conda install -c conda-forge opencv
#
conda install -c anaconda matplotlib
conda install --name vsBachelor pylint -y

```



### 1. Dataset
#### 1.1. Datamining the [scryfall api](https://scryfall.com/docs/api) in python
To construct a dataset suitable for training the CNN, I used the scryfall api 

### 2. CNN
