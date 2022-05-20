import os
import shutil
from PIL import Image


def images_rename(path):
    for folder in os.listdir(path):
        for image in os.listdir(path + '\\' + folder):
            os.rename(path + '\\' + folder + '\\' + image, path + '\\' + folder + '_' + image)
        shutil.rmtree(path + '\\' + folder)


def get_label(path):
    with open(path, 'r') as f:
        label = [line.strip('\n').split(',') for line in f.readlines()]
    return label


def split_label_by_frames(label, frames_num):
    labels = [[] for _ in range(frames_num)]
    for i in range(len(label)):
        labels[int(label[i][0]) - 1].append(label[i])
    return labels


def convert_box(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    return [str((int(box[0]) + int(box[2]) / 2) * dw), str((int(box[1]) + int(box[3]) / 2) * dh),
            str(int(box[2]) * dw), str(int(box[3]) * dh)]


def to_yolov5(labels, sizes):
    new_labels = [[[labels[i][j][k] for k in range(len(labels[i][j]))
                    if k != 0 and k != 1 and k != 6 and k != 8 and k != 9]
                   for j in range(len(labels[i]))] for i in range(len(labels))]

    yolov5_labels = [[[new_labels[i][j][4]] for j in range(len(new_labels[i]))] for i in range(len(new_labels))]

    for i in range(len(new_labels)):
        for j in range(len(new_labels[i])):
            yolov5_labels[i][j].extend(convert_box(sizes[i], new_labels[i][j]))

    return yolov5_labels


def labels_to_txt(right_labels, file, labels_path, images_path):
    os.remove(labels_path + '\\' + file)
    images = [image for image in os.listdir(images_path) if image.startswith(file.rstrip('.txt'))]

    for i in range(len(right_labels)):
        with open(labels_path + '\\' + images[i].rstrip('.jpg') + '.txt', 'w') as f:
            for j in range(len(right_labels[i])):
                f.write(' '.join(right_labels[i][j]))
                if j != len(right_labels[i]) - 1:
                    f.write('\n')


# train

train_images_path = r'D:\MSU\datasets\visdrone-vid\train\images'
train_labels_path = r'D:\MSU\datasets\visdrone-vid\train\labels'
copy_train_images_path = r'D:\MSU\VID\VisDrone2019-VID-train\VisDrone2019-VID-train\sequences'
copy_train_labels_path = r'D:\MSU\VID\VisDrone2019-VID-train\VisDrone2019-VID-train\annotations'

shutil.rmtree(train_images_path)
shutil.copytree(copy_train_images_path, train_images_path)

images_rename(train_images_path)

shutil.rmtree(train_labels_path)
shutil.copytree(copy_train_labels_path, train_labels_path)


# val

val_images_path = r'D:\MSU\datasets\visdrone-vid\val\images'
val_labels_path = r'D:\MSU\datasets\visdrone-vid\val\labels'
copy_val_images_path = r'D:\MSU\VID\VisDrone2019-VID-val\VisDrone2019-VID-val\sequences'
copy_val_labels_path = r'D:\MSU\VID\VisDrone2019-VID-val\VisDrone2019-VID-val\annotations'

shutil.rmtree(val_images_path)
shutil.copytree(copy_val_images_path, val_images_path)

images_rename(val_images_path)

shutil.rmtree(val_labels_path)
shutil.copytree(copy_val_labels_path, val_labels_path)


# test

test_images_path = r'D:\MSU\datasets\visdrone-vid\test\images'
test_labels_path = r'D:\MSU\datasets\visdrone-vid\test\labels'
copy_test_images_path = r'D:\MSU\VID\VisDrone2019-VID-test-dev\VisDrone2019-VID-test-dev\sequences'
copy_test_labels_path = r'D:\MSU\VID\VisDrone2019-VID-test-dev\VisDrone2019-VID-test-dev\annotations'

shutil.rmtree(test_images_path)
shutil.copytree(copy_test_images_path, test_images_path)

images_rename(test_images_path)

shutil.rmtree(test_labels_path)
shutil.copytree(copy_test_labels_path, test_labels_path)


# main

a = (train_labels_path, train_images_path)
b = (val_labels_path, val_images_path)
c = (test_labels_path, test_images_path)

for task_path in []:
    for i in os.listdir(task_path[0]):
        label = get_label(task_path[0] + '\\' + i)
        labels = split_label_by_frames(label, len([name for name in os.listdir(task_path[1])
                                                   if name.startswith(i.rstrip('.txt'))]))

        images_sizes = [Image.open(task_path[1] + '\\' + j).size for j in os.listdir(task_path[1])
                        if j.startswith(i.rstrip('.txt'))]

        right_labels = to_yolov5(labels, images_sizes)
        labels_to_txt(right_labels, i, task_path[0], task_path[1])


# lower the number of images and labels

images_path = val_images_path
labels_path = val_labels_path

l = os.listdir(images_path)

for n in l[::10]:
    target = images_path + '\\' + n
    if os.path.isfile(target):
        os.unlink(target)

l = os.listdir(labels_path)

for n in l[::10]:
    target = labels_path + '\\' + n
    if os.path.isfile(target):
        os.unlink(target)
