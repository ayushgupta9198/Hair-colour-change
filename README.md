#Hair colour changer

DeepDYE is a deep learning model to dye hair un photographs using neural networks.

## How does it works?
1. Process the image with segmentation model based on U-Net to locate the hair area.
2. Color the hair area with the desired color.
3. Merge the images with a soft-light blend mode.

Soft-light blend is powered by [https://github.com/flrs/blend_modes](https://github.com/flrs/blend_modes)

## Installation
1. Clone the repo
```
git clone https://github.com/alcros33/DeepDYE
```
2. Make a virtual env and install the requirements
```
virtualenv .env
source .env/bin/activate
pip install Pillow opencv-python
```
3. Follow the instructions to install Pytorch, then install torchvision and fastai
```
# https://pytorch.org/get-started/locally/
pip install torchvision
pip install fastai
```
4. Download the model and place it inside the folder `Models`

[https://drive.google.com/open?id=10AfHydtWC1rtEyvjyMR9ue02aBsQU5Vv](https://drive.google.com/open?id=10AfHydtWC1rtEyvjyMR9ue02aBsQU5Vv)

##  Usage
```
All you need to do is create folders like input and output and run the below command to execute:

python DeepDYE.py Image.jpg [red|green|blue|pink] -o ImageOut.png
```
