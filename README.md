# ImageNet-
Process ImageNet 2012 dataset

# Environment Setup
## If you are using Anaconda or Miniconda
run `conda env create -f environment.yml`  
then run `conda activate imagenet`
## Otherwise
run `pip install -r requirements.txt`

# Run
1. Create a folder called "imagenet"
2. From [ImageNet Website](https://image-net.org/), Download 4 files in the ImageNet 2012 dataset 
    * Development kit (Task 1 & 2) (ILSVRC2012_devkit_t12.tar.gz)
    * Training images (Task 1 & 2) (ILSVRC2012_img_train.tar_file)
    * Validation images (all tasks) (ILSVRC2012_img_val.tar)
    * Test images (all tasks)] (ILSVRC2012_img_test_v10102019.tar)
3. Put the above 4 files in the "imagenet" folder
4. Put the `imagenet.py` file in the "imagenet" folder
5. In the "imagenet" folder, run `python imagenet.py`

# Import Dataset in PyTorch
```
    # import data
    data=datasets.ImageFolder(
        root=root_dir, # TODO: put your own imagenet directory(<your dir>/imagenet/train)
        transform=compose,
    )
    # create data loader
    data_loader = torch.utils.data.DataLoader(
        data,
        batch_size=BATCH_SIZE, # TODO: set your own batch size
        shuffle=True
    )
    # use the dataset
    for n_batch, (images, labels) in enumerate(data_loader):
        #TODO: your code here
```

# Expected Result
* 'x' represents a digit from 0 to 9  
imagenet/  
├─ devkit/  
│  ├─ ILSVRC2012_devkit_t12/  
│  │  ├─ data/  
│  │  │  ├─ ILSVRC2012_validation_ground_truth.txt  
│  │  │  ├─ meta.mat  
│  │  ├─ evaluation/  
│  │  │  ├─ .m code files for evaluation  
│  │  ├─ COPYING  
│  │  ├─ readme.txt  
├─ test/  
│  ├─ test/  
│  │  ├─ ILSVRC2012_test_xxxxxxxx.JPEG (100000 image)  
├─ train/  
│  ├─ nxxxxxxx (1000 folders, each folder contains a bunch of images with the same category)/  
│  │  ├─ nxxxxxxx_xxx,JPEG (around 1300 picture each folders)  
├─ val/  
│  ├─ xxx (1000 folders from 1 to 1000)/  
│  │  ├─ ILSVRC2012_val_xxxxxxxx.JPEG (several val images)  
├─ ILSVRC2012_devkit_t12.tar.gz  
├─ ILSVRC2012_img_test_v10102019.tar  
├─ ILSVRC2012_img_train.tar_file  
├─ ILSVRC2012_img_val.tar  
├─ imagenet.py  
├─ train_labels.csv (file maps each WNID to the cooresponding label, categorities, and explanation)  
