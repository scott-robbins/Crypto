import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io as io
import numpy as np
import utils
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
    if len(sys.argv) > 1 and '-dims' not in sys.argv:
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
            plt.imsave(fname.split('.')[0]+'.png', image_data)
        if ext == 'pdf':
            image_data = process_text(swap(fname, False), True)
            plt.imsave(fname.split('.')[0] + '.png', image_data)
        if ext == 'wav':
            data = load_wav(fname)
        if ext == 'mat':
            data = load_mat(fname)
        # Show the image
        plt.imshow(image_data, 'gray')
        plt.show()
    elif len(sys.argv) >=2 and '-dims' in sys.argv:
        fname = sys.argv[1]
        try:
            ext = sys.argv[1].split('.')[1]
            if ext in types:
                print "Processing " + ext
            sys.argv.remove(fname)
            sys.argv.pop(0)
            sys.argv.pop(0)
        except IndexError:
            print "Incorrect Syntax!"
            exit(0)
        dims = [int(sys.argv[0]), int(sys.argv[1])]
        state = np.zeros(dims)
        # Handle various file types and get all the data
        if ext == 'txt':
            data = swap(fname, False)
            test = process_text(data, False)
        if ext == 'pdf':
            data = swap(fname, False)
            test = process_text(data, False)

        if ext == 'wav':
            data = load_wav(fname)
        if ext == 'mat':
            data = load_mat(fname)

        cx = dims[0]/2
        cy = dims[1]/2

        padx = dims[0] - test.shape[0]
        pady = dims[1] - test.shape[1]

        state[cx-test.shape[0]/2:cx+test.shape[0]/2,
              cy-test.shape[1]/2:cy+test.shape[1]/2] = test

        print 'x_pad: ' + str(padx) + '\ty_pad: ' + str(pady)
        print 'Min: ' + str(state.min())
        print 'Max: ' + str(state.max())

        register = np.zeros((pady/2, padx/2))
        p = int(np.sqrt(padx*pady/4))
        if len(register.flatten()) < (state.max()-state.min()) and register.shape[0]-state.shape[0]>p and register.shape[0]-state.shape[1]>p :
            print 'Illegal Bitmapping!'
            exit(0)
        # counter = 0
        # for ii in range(len(register.flatten())):
        #     [x,y] = utils.ind2sub(ii,register.shape)
        #     register[x-5:x+10,y-5:y+10] = counter
        #     counter += 1
        #     if counter >= (state.max()-state.min()):
        #         counter = 0
        # register = register.reshape((pady/2,padx/2))
        gscale = np.arange(state.min(), state.max(), 1)
        for col in range(int(state.max()-state.min())):
            register[col-10:col,:] = gscale[col]
        print register.shape
        # Add Left Register
        state[p:pady/2+p,p:padx/2+p] = np.rot90(np.rot90(register))
        # Add Right Register (Rotate 180 Degrees)
        state[state.shape[0]-pady/2-p:state.shape[0]-p,
              state.shape[1]-padx/2-p:state.shape[1]-p] = register

        plt.imshow(state, 'gray')
        plt.show()

        if 'save' in sys.argv:
            plt.imsave(fname.split('.')[0]+'.png', state)


if __name__ == '__main__':
    main()
