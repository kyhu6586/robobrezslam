import numpy as np
import math
import matplotlib.pyplot as plt
import contextlib
import io
from scipy.signal import convolve2d
from scipy.ndimage.interpolation import rotate
from array2gif import write_gif

def save_data(filename,imgbytes, imgsize):
    '''
        Saves the data as an array
    '''
    wid, hgt = imgsize

    data_array = np.zeros(imgsize,dtype=int)

    for y in range(hgt):
        for x in range(wid):
            data_array[x][y] = imgbytes[y * wid + x]
    data_array = data_array<125
    data_array = data_array*1
    data_array = rotate(data_array,angle=90)
    data_array = np.flipud(data_array)
    np.save(filename,data_array)
    data_array.tolist()
    return data_array

def fix_data(imgbytes, imgsize, theta, x_shift, y_shift):
    '''
        Reorients the map by theta degrees and shifts it accordingly
    '''
    wid, hgt = imgsize

    data_array = np.zeros(imgsize,dtype=int)

    for y in range(hgt):
        for x in range(wid):
            data_array[x][y] = imgbytes[y * wid + x]
    theta = math.degrees(theta)
    data_array = data_array<125
    data_array = data_array*1
    data_array = rotate(data_array,angle=theta)
    data_array = np.flip(data_array)
    # np.save(filename,data_array)
    data_array.tolist()
    return data_array


def convolve_map(output_file,input_file,kernel):
    data = np.load(input_file)
    h = np.ones((kernel,kernel))
    convolved_data = convolve2d(data,h)
    convolved_data = convolved_data>0.5
    convolved_data = convolved_data*1    
    np.save(output_file,convolved_data)
    return convolved_data

def save_data_to_csv(filename, imgbytes, imgsize):
    '''
        Saves the data into a csv file
    '''
    #TO DO
    wid, hgt = imgsize
    return 1

def save_data_to_png(filename, imgbytes, imgsize):
    '''
        Saves the data as a png file
    '''   
    wid, hgt = imgsize
    data_array = np.zeros(imgsize,dtype=int)

    for y in range(hgt):
        for x in range(wid):
            data_array[x][y] = imgbytes[y * wid + x]
    data_array = rotate(data_array,angle=90)
    data_array = np.flipud(data_array)
    plt.imshow(data_array)
    plt.savefig(filename) 

def save_data_to_movie(filename, imgbytes, imgsize):
    '''
        Saves the data as a pkv
    '''
    #TO DO
    return 1

def comma_to_space(filename,newfilename):
    '''
        Converts a file delimited by commas to space delimited
        Returns a newly written file with the fix.
    '''
    with open (filename) as input_file:
        s = input_file.read().replace(',', ' ')
    with open (newfilename+'.dat', 'w') as output_file:
        output_file.write(s)
    return newfilename

def inf_to_zero(filename,newfilename):
    '''
        Converts 'inf' to 0.
        Returns a newly written file with the fix.
    '''
    with open (filename) as input_file:
        s = input_file.read().replace('inf', '0')
    with open (newfilename+'.dat', 'w') as output_file:
        output_file.write(s)
    return newfilename

def remove_empty_line(filename,newfilename):
    with open (filename) as input_file:
        s = input_file.read().replace('\n\n', '\n')
    with open (newfilename+'.dat', 'w') as output_file:
        output_file.write(s)
    return newfilename

def visualize_output(filename):
    data = np.load(filename)
    plt.imshow(data)
    plt.savefig(filename+'.png')