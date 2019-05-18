import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io as io
import numpy as np
import sys
import os

types = ['csv', 'txt', 'pdf',
         'png', 'jpg', 'jpeg',
         'avi', 'mp4', 'webm',
         'wav', 'mp3', 'mat']


def load_wav(file_name):
    return wavfile.read(file_name)


def load_mat(file_name):
    return io.loadmat(file_name)


def swap(file_name, destroy):
    data = []
    [data.append(line.replace('\n', '')) for line in open(file_name, 'r')]
    if destroy:
        os.remove(file_name)
    return data


def process_text(text_data, show):
    block_size = 0
    values = list()
    for line in text_data:
        characters = list(line)
        for element in characters:
            values.append(ord(element))
    sz = len(values)
    print str(sz) + ' Bytes Loaded'

    if np.sqrt(sz) % 1 == 0:
        block_size = np.sqrt(sz)
        print "Block Size = " + str(np.sqrt(sz))
    elif np.ceil(np.sqrt(sz)) % 1 == 0:
        print "Block Size = " + str(np.ceil(np.sqrt(sz)))
        block_size = int(np.ceil(np.sqrt(sz)))
    blank = np.zeros((block_size, block_size)).flatten()
    content = np.array(values)
    for i in range(len(blank)):
        try:
            blank[i] = content[i]
        except IndexError:
            blank[i] = 0
    blank = blank.reshape((block_size,block_size))
    if show:
        plt.imshow(blank, 'gray_r')
        plt.show()
    return blank


def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        try:
            ext = sys.argv[1].split('.')[1]
            if ext in types:
                print "Processing " + ext
        except IndexError:
            print "Incorrect Syntax!"
            exit(0)
        # Handle various file types and get all the data
        if ext == 'txt':
            data = swap(fname, False)
            image_data = process_text(data, False)
            plt.imsave('data.png', image_data)
        if ext == 'pdf':
            image_data = process_text(swap(fname, False), True)
            plt.imsave('data.png', image_data)
        if ext == 'wav':
            data = load_wav(fname)
        if ext == 'mat':
            data = load_mat(fname)


if __name__ == '__main__':
    main()
