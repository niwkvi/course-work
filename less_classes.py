import os

labels_path = r'D:\MSU\datasets\visdrone-vid\train\labels'
images_path = r'D:\MSU\datasets\visdrone-vid\train\images'


def get_label(path):
    with open(path, 'r') as f:
        label = [line.strip('\n').split(' ') for line in f.readlines()]
    return label


def change_label(label):

    new_label = [label[i] for i in range(len(label)) if label[i][0] != '0' and label[i][0] != '11']
    
    for i in range(len(new_label)):
        if new_label[i][0] == '1':
            new_label[i][0] = '0'
        elif new_label[i][0] == '2':
            new_label[i][0] = '0'
        elif new_label[i][0] == '3':
            new_label[i][0] = '1'
        elif new_label[i][0] == '4':
            new_label[i][0] = '2'
        elif new_label[i][0] == '5':
            new_label[i][0] = '2'
        elif new_label[i][0] == '6':
            new_label[i][0] = '2'
        elif new_label[i][0] == '7':
            new_label[i][0] = '1'
        elif new_label[i][0] == '8':
            new_label[i][0] = '1'
        elif new_label[i][0] == '9':
            new_label[i][0] = '2'
        elif new_label[i][0] == '10':
            new_label[i][0] = '1'

    return new_label


def print_new_label(new_label, path):
    with open(path, 'w') as f:
        for i in range(len(new_label)):
            for j in range(len(new_label[i])):
                f.write(new_label[i][j])
                if j != len(new_label[i]):
                    f.write(' ')
            if i != len(new_label):
                f.write('\n')


for i in os.listdir(labels_path):
        label = get_label(labels_path + '\\' + i)
        new_label = change_label(label)
        print_new_label(new_label, labels_path + '\\' + i)
