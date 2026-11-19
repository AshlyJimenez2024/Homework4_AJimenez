#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image blurring library.
@author: icardei
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

import timeit       # for benchmarking

def image_load(filename):
    """Load an image file into an ndarray."""
    return plt.imread(filename)

def image_save(filename, img):
    """Save an image img into a file with a given name filename."""
    plt.imsave(filename, img)
    

def fmt_save_filename(origfilename, modif):
    """Format an image file name."""
    return "{}_{}.png".format(origfilename.split(".")[-2], modif)


def img_blur0_naive(img):
    """ A naive implementation for 3x3 blurring with nested Python loops."""
    (h, w, _) = img.shape
    offsets = [-1, 0, 1]
    blr = np.zeros(img.shape, dtype=np.uint8)
    for r in range(h):
        for c in range(w):
            # each (3,) shape RGB pixel is the average of its eight neighbors plus itself.
            count = 0
            pixsum = np.zeros((3,), dtype=np.uint32)
            for i in offsets:
                for j in offsets:
                    row = r + i
                    col = c + j
                    # check if the current pixel has valid coordinates
                    if 0 <= row < h and 0 <= col < w:
                        count += 1
                        pixsum += img[row, col, :]   # work with RGB (3,) arrays
            blr[r, c] = pixsum / count     # the average
    return blr


def img_blur_naive(img, weights):
    """ A naive implementation for weighted blurring with nested Python loops.
    This is a 2D convolution computation between img and the weights matrix.
    The complexity is Theta(img.shape[0] * img.shape[1] * weights.size * 3)
    img is the image ndarray
    weights is the n x n matrix used for the convolution, i.e. the weights.
    """
    (h, w, _) = img.shape
    offsets = [-1, 0, 1]   # offset relative to current (r,c) position
    blr = np.zeros(img.shape, dtype=np.uint8)
    for r in range(h):
        for c in range(w):
            # do this for each row r and column c:
            total_weight = 0
            # sum of all pixel values for this neighborhood
            pixsum = np.zeros((3,), dtype=np.float64)   
            # for each neighbor pixel:
            for i in range(len(offsets)):
                for j in range(len(offsets)):
                    row = r + offsets[i]     # row of current pixel
                    col = c + offsets[j]     # column of current pixel
                    # compute weighted sum only for neighbors that have valid coordinates:
                    if 0 <= row < h and 0 <= col < w:  
                        total_weight += weights[i, j]
                        # compute a weighted average 
                        pixsum += weights[i, j] * img[row, col, :]
            blr[r, c] = pixsum / total_weight    # gets truncated to uint8 type
    return blr


def img_blur(img, weights):
    """ A faster implementation for weighted blurring with numpy.
    img is the image ndarray
    weights is the n x n matrix used for the convolution, i.e. the weights.
    """
    (h, w, _) = img.shape
    hoffsets = np.arange(weights.shape[1], dtype=np.int32) - int(weights.shape[1] / 2)
    voffsets = np.arange(weights.shape[0], dtype=np.int32) - int(weights.shape[0] / 2)
    sums = np.zeros(img.shape, dtype=np.float64)
    total_weight = 0
    for i in voffsets:
        for j in hoffsets:
            # print(i + int(weights.shape[0] / 2), j + int(weights.shape[1] / 2))
            weight = weights[i + int(weights.shape[0] / 2), j + int(weights.shape[1] / 2)] 
            total_weight += weight
            # slice ranges for img and for the blurred image array, sums
            tsum = (max(0, i),min(h + i, h), max(0,j), min(w+j, w))
            ta = (max(0,-i), min(h, h-i), max(0, -j), min(w-j,w))
            (sr0, sr1, sc0, sc1) = tsum
            (ar0, ar1, ac0, ac1) = ta
            # update weighted sum with the current slice and current weight:
            sums[sr0:sr1, sc0:sc1] += img[ar0:ar1, ac0:ac1].astype(np.float64) * weight
    # scale each pixel value by 1/total_weight
    b = (sums / total_weight).astype(np.uint8)  # convert pixel values to uint8
    return b


def show_imgs(*imgs):
    """ Display a sequence of images using matplotlib."""
    ncols = len(imgs)
    nrows = 1

    if len(imgs) > 1:
        (fig, axes) = plt.subplots(nrows=nrows, ncols=ncols)    # axes is  nrows x ncols axis ndarray
    
        k = 0
        for (axis, img) in zip(axes.flat, imgs):
            img = axis.imshow(img, interpolation='none')    # create subplot image
            axis.set_title("Image {}".format(k))
            axis.set_axis_off()     
            k += 1
    else:
        plt.ishow(imgs[0])
    plt.show()


def test1():
    fn = "florida-keys-800-480.jpg"
    img1 = image_load(fn)
    # img0n = img_blur0_naive(img1)
    imgn = img_blur_naive(img1, np.array([[1, 1, 1], [1, 4, 1], [1, 1, 1]]))

    # print((img0n == imgn).all())
    
    saved_filename = fmt_save_filename(fn, "141")
    image_save(saved_filename, imgn)
    print("File {} blurred and saved to {}.".format(fn, saved_filename))
    
def test2():
    fn = "florida-keys-800-480.jpg"
    img1 = image_load(fn)
    # img0n = img_blur0_naive(img1)
    mainweight = [1, 0, 3, 10, 20]
    imgbs = [img_blur(img1, np.array([[1, 1, 1], [1, bl, 1], [1, 1, 1]])) for bl in mainweight]
    # img3n = img_blur(img1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))

    # print((img0n == imgn).all())
    for i in range(len(mainweight)):
        saved_filename = fmt_save_filename(fn, "3x3-{}".format(mainweight[i]))
        image_save(saved_filename, imgbs[i])
        print("File {} blurred and saved to {}.".format(fn, saved_filename))
    show_imgs(*imgbs)


def test3():
    fn = "florida-keys-800-480.jpg"
    img1 = image_load(fn)
    # img0n = img_blur0_naive(img1)
    weightsize = [3,5,7,11,17,25]
    imgbs = [img_blur(img1, np.ones((ws, ws))) for ws in weightsize]

    for i in range(len(weightsize)):
        saved_filename = fmt_save_filename(fn, "{}x{}-{}".format(weightsize[i], weightsize[i], 1))
        image_save(saved_filename, imgbs[i])
        print("File {} blurred and saved to {}.".format(fn, saved_filename))
    show_imgs(*imgbs)


def make_samples_avg():
    fn = "cactus-flower-261.jpg"
    img1 = image_load(fn)
    krn = np.ones((9,9))   # use a 9x9 weight matrix with all value equal to 1
    img2 = img_blur(img1, krn)
    # save the file with a name that includes blr-9x9 before the extension: "cactus-flower-261_blr-9x9.png"
    image_save(fmt_save_filename(fn, "blr-{}x{}".format(krn.shape[0], krn.shape[1])), img2)
    
    
def make_samples_weight_sizes():
    fn = "cactus-flower-261.jpg"
    img1 = image_load(fn)
    wss = [3, 11, 19]
    krns = [np.ones((ws, ws)) for ws in wss]
    imgbls = [img_blur(img1, krn) for krn in krns]
    for i in range(len(wss)):
        krn = krns[i]
        image_save(fmt_save_filename(fn, "blr-{}x{}".format(krn.shape[0], krn.shape[1])), imgbls[i])
    
    
def make_samples_weightcenter():
    def makew(ws, centerw):
        w = np.ones((ws, ws))
        w[ws // 2, ws // 2] = centerw
        return w
    
    fn = "cactus-flower-261.jpg"
    img1 = image_load(fn)
    ws = 7
    cws = [1, 10, 100, 1000]
    krns = [makew(ws, cw) for cw in cws]
    imgbls = [img_blur(img1, krn) for krn in krns]
    for i in range(len(cws)):
        krn = krns[i]
        image_save(fmt_save_filename(fn, "blr-{}x{}_cw{}".format(krn.shape[0], krn.shape[1], cws[i])), imgbls[i])
    
 
#test3()
 
    
def benchmark_blur():
    """ Compare the runtime for the different blurring algorithms."""
    from scipy import ndimage
    
    fn = "florida-keys-800-480.jpg"
    img1 = image_load(fn)
    number = 3
    weights = np.ones((3, 3))
    seconds_naive = timeit.timeit(lambda : img_blur_naive(img1, weights), number=number) / number
    seconds_fastblur =  timeit.timeit(lambda : img_blur(img1, weights), number=number)  / number  
    seconds_scipy =  timeit.timeit(lambda : ndimage.uniform_filter(img1, size=3), number=number)  / number  
    print("blur naive 3x3: ", seconds_naive, " seconds")
    print("blur fast 3x3: ", seconds_fastblur, " seconds")
    print("blur scipy 3x3: ", seconds_scipy, " seconds")

    # also scipy.ndimage.gaussian_filter