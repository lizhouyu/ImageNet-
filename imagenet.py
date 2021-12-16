import os
import tarfile
import time
import shutil
from scipy.io import loadmat
import csv

DEVKIT_FILE_NAME = "ILSVRC2012_devkit_t12.tar.gz"
TRAIN_FILE_NAME = "ILSVRC2012_img_train.tar"
VAL_FILE_NAME = "ILSVRC2012_img_val.tar"
TEST_FILE_NAME = "ILSVRC2012_img_test_v10102019.tar"

def untar(file, target_dir="", is_show_detail=False):
    file_name = file.split('.')[0]
    file_ext = file.split('.')[-1]
    mode = 'r'
    if file_ext == 'gz':
        mode = 'r:gz'
    if is_show_detail:
        print("read the file" + file)
    tar_file = tarfile.open(file, mode)
    if is_show_detail:
        print("check or create directory")
    if target_dir == "":
        target_dir = file_name
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    files = tar_file.getnames()
    if is_show_detail:
        total_files = len(files)
        current_file_index = 1
        print("start to extract files")
    for f in files:
        if is_show_detail:
            print("[" + str(current_file_index) + "/" + str(total_files) + "] extracting: " + f)
        tar_file.extract(f, target_dir)
        if is_show_detail:
            print("[" + str(current_file_index) + "/" + str(total_files) + "] successfully extracted: " + f)
            current_file_index += 1
    tar_file.close()

def clear_folder(folder):
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                os.remove(os.path.join(root, file)) 
                print("remove " + os.path.join(root, file))
            for directory in dirs:
                clear_folder(os.path.join(root, directory)) 
        os.rmdir(folder)

if __name__ == '__main__':
    
    #unzip dev kit
    print("{1/4} extract development kit ")
    DEVKIT_NAME = DEVKIT_FILE_NAME.split('.')[0]
    untar(DEVKIT_FILE_NAME, "devkit")
    print("{1/4} parse the validation ground truth")
    val_index_label_pairs = {}
    path_devkit_data = os.path.join("devkit",DEVKIT_NAME)
    path_devkit_data = os.path.join(path_devkit_data,"data")
    path_val_ground_truth = os.path.join(path_devkit_data,"ILSVRC2012_validation_ground_truth.txt")
    file_val_ground_truth = open(path_val_ground_truth, "r")
    lines = file_val_ground_truth.readlines()
    line_index = 1
    for line in lines:
        val_index_label_pairs[line_index]=line.strip('\n')
        line_index += 1
    print("{1/4} validation ground truth cached")
    print("{1/4} create the wnid-label-category-explanation form")
    headers = ['wnid', 'label', 'category', 'explanation']
    rows = []
    path_train_labels = os.path.join(path_devkit_data,"meta.mat")
    train_labels = loadmat(path_train_labels)
    train_labels = train_labels['synsets']
    for i in range(len(train_labels)):
        row = {'wnid': train_labels[i][0][1][0], 'label': train_labels[i][0][0][0][0], 'category':train_labels[i][0][2][0], 'explanation': train_labels[i][0][3][0]}
        rows.append(row)
    with open('train_labels.csv', 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
    print("{1/4} wnid-label-category-explanation form created")
    print("{1/4} development kit successfully extracted")


    #unzip the training data
    print("{2/4} extract training data")
    print("{2/4} clean the train folder")
    clear_folder("train")
    print("{2/4} unzip the training dataset, may take a longer time")
    untar(TRAIN_FILE_NAME, "train", is_show_detail=True)
    print("{2/4} unzip the subfolders of training dataset, may take a longer time")
    train_tar_files = os.listdir("train")
    total_train_tar_files = len(train_tar_files)
    train_tar_file_counter = 0
    for train_tar_file in train_tar_files:
        untar("train/"+train_tar_file, is_show_detail=False)
        os.remove("train/"+train_tar_file)
        train_tar_file_counter += 1
        print("[" + str(train_tar_file_counter) + "/" + str(total_train_tar_files) + "] extracted: " + train_tar_file)
    print("{2/4} trainning data successfully extracted")


    #unzip the validation data
    print("{3/4} extract validation data")
    print("{3/4} clean the validation folder")
    clear_folder("val")
    print("{3/4} unzip the validation dataset, may take a longer time")
    untar(VAL_FILE_NAME, "val", is_show_detail=True)
    val_images = os.listdir('val')
    num_val_images = len(val_images)
    val_image_counter = 0
    for image in val_images:
        image_path = os.path.join("val", image)
        image_index = int(image.split('.')[0].split('_')[-1])
        image_target_dir = os.path.join("val", val_index_label_pairs[image_index])
        if not os.path.exists(image_target_dir):
            os.mkdir(image_target_dir)
        shutil.move(image_path, image_target_dir)
        val_image_counter += 1
        print("[" + str(val_image_counter) + "/" + str(num_val_images) + "] moved: " + image)
    print("{3/4} validation data successfully extracted")


    #unzip the test data
    print("{4/4} extract testing data")
    print("{4/4} clean the test folder")
    clear_folder("test")
    print("{4/4} unzip the test dataset, may take a longer time")
    untar(TEST_FILE_NAME, "test", is_show_detail=True)
    print("{4/4} testing data successfully extracted")

    print("Finished!")
