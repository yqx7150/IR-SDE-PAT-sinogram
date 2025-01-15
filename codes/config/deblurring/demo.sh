#!/bin/bash

#############################################################
### training ###
CUDA_VISIBLE_DEVICES=0 python train.py -opt=options/train/ir-sde.yml
CUDA_VISIBLE_DEVICES=0 python train.py -opt=options/train/refusion-leejh.yml
# for single GPU
python train.py -opt=options/train/ir-sde.yml
# python train.py -opt=options/train/refusion.yml

# for multiple GPUs
# python -m torch.distributed.launch --nproc_per_node=2 --master_port=6512 train.py -opt=options/train/ir-sde.yml --launcher pytorch
# python -m torch.distributed.launch --nproc_per_node=2 --master_port=6512 train.py -opt=options/train/refusion.yml --launcher pytorch

#############################################################

### testing ###
python test.py -opt=options/test/ir-sde.yml
python test.py -opt=options/test/refusion-leejh.yml

### train resume
# #### path #resume train
# path:
#   pretrain_model_G: /home/b110/code/LZL/irsde/codes/config/deblurring/log/xueguan16-512-100BW-leejh0826-300T/models/130000_G.pth
#   strict_load: true
#   resume_state: /home/b110/code/LZL/irsde/codes/config/deblurring/log/xueguan16-512-100BW-leejh0826-300T/training_state/130000.state




#############################################################