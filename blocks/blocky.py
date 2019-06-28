import matplotlib.pyplot as plt
import numpy as np
import shutil
import time
import sys
import os

IS_LINUX = False
T0 = time.time()
if os.name != 'nt':
    IS_LINUX = True


def swap(fname, destroy):
    data = []
    [data.append(line.replace('\n', '')) for line in open(fname, 'r')]
    if destroy:
        os.remove(fname)
    return data


if len(sys.argv) > 1:
    target_file = sys.argv.pop()
    data = []

    for line in swap(target_file, False):
        for element in list(line):
            data.append(ord(element))
    print '==========================================================' \
          '\nReading \033[1m'+target_file+'...\033[0m'
    print '  * Data Length: %d' % len(data)
    print '  * Min Value: %s' % np.array(data).min()
    print '  * Max Value: %s' % np.array(data).max()

    BlockSize = int(np.ceil(np.sqrt(len(data))))
    print 'Using BLOCKSIZE: %d' % BlockSize

    # TODO: Create Image Using BlockSize
    N_Pads = BlockSize*BlockSize - len(data)
    [data.append(0.) for p in range(N_Pads)]
    stacks = np.array(data).astype(np.int).reshape((BlockSize,BlockSize))
    print np.array(stacks).shape

    inv_im = np.array(data).max()*np.ones(stacks.shape) - stacks
    im = stacks

    plt.imshow(im*inv_im,'gray')
    plt.show()


print '\033[1m\033[31mFINISHED [%ss Elapsed]\033[0m' % (time.time() - T0)
