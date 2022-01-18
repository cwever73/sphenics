#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 09:40:25 2022

@author: carl
"""

import itertools
import numpy as np
from PIL import Image
import sys
import time



def gen_primes(max_index):
    """Function:
    Sieve of Eratosthenes
    Code by David Eppstein, UC Irvine, 28 Feb 2002
    http://code.activestate.com/recipes/117119/
    Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    
    # The running integer that's checked for primeness
    q = 2
    
    while len(D) < max_index:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            # 
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next 
            # multiples of its witnesses to prepare for larger
            # numbers
            # 
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1


def get_sphenics(lst_lst, dct_tf):
    
    combos = list(itertools.product(*lst_lst))
    
    sphenics_dct = {}
    
    for combo in combos:
        prdct = 1
        for i in combo:
            prdct *= i
        
        sphenics_dct[prdct] = combo
         
    if dct_tf:
        return sphenics_dct
    
    else:
        return list(sphenics_dct.keys())

def rgb2prm(fn, n_imgs=10):
    
    #grab batch of images
    dct = unpickle(fn)
    
    if n_imgs > len(dct[b'data']):
       n_imgs = len(dct[b'data']) 
       print(f"""WARNING: Amount of images requested is larger than dataset. 
             Processing {len(dct[b'data'])} image""")

    else:
        print(f'Processing {n_imgs} images.')
        
        
    prm_img_dct = {}    
    for i in range(n_imgs):
        print(i)
        img = dct[b'data'][i]
        
        tst_img_r = img[:1024]
        # r = np.reshape(tst_img_r, (32,32))
        tst_img_g = img[1024:2048]
        # g = np.reshape(tst_img_g, (32,32))
        tst_img_b = img[-1024:]
        # b = np.reshape(tst_img_b, (32,32))
        
        #put it in (32,32,3) uint8 np array
        # img_array = np.dstack((r,g,b))
        
        
        #go get that list of sphenics
        max_index = 768
        primes = gen_primes(max_index)
        data_dct = split_primes(primes)
    
        prm_array_r = tuple([data_dct['prime_r'][tst_img_r[i]] 
                       for i in range(len(tst_img_r))])
        prm_array_g = tuple([data_dct['prime_g'][tst_img_g[i]] 
                       for i in range(len(tst_img_g))])
        prm_array_b = tuple([data_dct['prime_b'][tst_img_b[i]] 
                       for i in range(len(tst_img_b))])
        
        
        prm_prdct_lst = []
        for indx in range(len(prm_array_r)):
            prdct = prm_array_r[indx]*prm_array_g[indx]*prm_array_b[indx]
            prm_prdct_lst.append(prdct)
            
        prm_array = np.reshape(np.asarray(prm_prdct_lst), (32,32))
        
        prm_img_dct[i] = prm_array
    
    return prm_img_dct
    


def split_primes(gen_o_primes):
    
    r = 1
    g = 2
    b = 3
    
    prime_r = []
    prime_g = []
    prime_b = []
    
    for i, n in enumerate(gen_o_primes, 1):
        # print(r,g,b,i,n)
        if i == r:
            prime_r.append(n)
            r += 3
        
        elif i == g:
            prime_g.append(n)
            g += 3
            
        elif i == b:
            prime_b.append(n)
            b += 3
            
        else:
            print('Something is wrong')
        
    dct_primes = {}
    
    #len is 257 for each list, shave off last number
    dct_primes['prime_r'] = prime_r[:-1] 
    dct_primes['prime_g'] = prime_g[:-1]
    dct_primes['prime_b'] = prime_b[:-1]
        
    return dct_primes

def unpickle(file):
    '''From CIFAR-10 README (http://www.cs.toronto.edu/~kriz/cifar.html):   
    data -- a 10000x3072 numpy array of uint8s. 
            Each row of the array stores a 32x32 colour image. 
            The first 1024 entries contain the red channel values, 
            the next 1024 the green, and the final 1024 the blue. 
            The image is stored in row-major order, 
            so that the first 32 entries of the array are the red 
            channel values of the first row of the image.
    labels -- a list of 10000 numbers in the range 0-9. 
            The number at index i indicates the label of the ith image 
            in the array data.
'''
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
            

if __name__ == "__main__":
    t0 = time.time()
    
    if sys.argv[1] == 'chck_sphncs':
        max_index = 768
        primes = gen_primes(max_index)
        
        data_dct = split_primes(primes)
        lst_lst = []
        for i in data_dct:
            lst_lst.append(data_dct[i])
            
        
        sphenics_lst = get_sphenics(lst_lst, False)
        
        print(f'Length of Sphenics List is {len(sphenics_lst)}')
        print(f'Length of Set of Sphenics List is {len(set(sphenics_lst))}')
        t1 = time.time()
        print(f'Took {round(t1-t0, 2)} seconds to run')
        
    if sys.argv[1] == 'get_first_img':
        fn = r'/home/carl1/projects/cifar-10-batches-py/data_batch_1'
        dct = unpickle(fn)
        dct.keys()
        
        tst_img = dct[b'data'][100]
        
        tst_img_r = tst_img[:1024]
        r = np.reshape(tst_img_r, (32,32))
        tst_img_g = tst_img[1024:2048]
        g = np.reshape(tst_img_g, (32,32))
        tst_img_b = tst_img[-1024:]
        b = np.reshape(tst_img_b, (32,32))
        
        array = np.dstack((r,g,b))
        
        img = Image.fromarray(array)
        img.save('testrgb.png')
        print('Test image saved in cd.')
        t1 = time.time()
        print(f'Took {round(t1-t0, 2)} seconds to run')
        
    if sys.argv[1] == 'transform_first_img':
        
        fn = r'/home/carl1/projects/cifar-10-batches-py/data_batch_1'
        
        #grab that first froggo image
        dct = unpickle(fn)
        dct.keys()
        
        tst_img = dct[b'data'][0]
        
        tst_img_r = tst_img[:1024]
        r = np.reshape(tst_img_r, (32,32))
        tst_img_g = tst_img[1024:2048]
        g = np.reshape(tst_img_g, (32,32))
        tst_img_b = tst_img[-1024:]
        b = np.reshape(tst_img_b, (32,32))
        
        #put it in (32,32,3) uint8 np array
        img_array = np.dstack((r,g,b))
        print('Original Image Array Shape: ',img_array.shape)
        print('Original Image Array Shape First Rows:\n Red: ', 
              img_array[:,0,0], '\n Green:' ,img_array[:,0,1], '\n Blue: ',
              img_array[:,0,2])
        
        
        #go get that list of sphenics
        max_index = 768
        primes = gen_primes(max_index)
        data_dct = split_primes(primes)

            
        prm_array_r = tuple([data_dct['prime_r'][tst_img_r[i]] 
                       for i in range(len(tst_img_r))])
        prm_array_g = tuple([data_dct['prime_g'][tst_img_g[i]] 
                       for i in range(len(tst_img_g))])
        prm_array_b = tuple([data_dct['prime_b'][tst_img_b[i]] 
                       for i in range(len(tst_img_b))])
        
        print('Prime Index for Original Array First Pixel (Row0, Col0) for Each Color:\n Red: ',
              data_dct['prime_r'][img_array[0,0,0]], '\n Green: ',
              data_dct['prime_g'][img_array[0,0,1]], '\n Blue: ',
              data_dct['prime_b'][img_array[0,0,2]])
        
        print('Prime Index for Original Array Second Pixel (Row0, Col1) for Each Color:\n Red: ',
              data_dct['prime_r'][img_array[0,1,0]], '\n Green: ',
              data_dct['prime_g'][img_array[0,1,1]], '\n Blue: ',
              data_dct['prime_b'][img_array[0,1,2]])
        
        
        prm_prdct_lst = []
        for i in range(len(prm_array_r)):
            prdct = prm_array_r[i]*prm_array_g[i]*prm_array_b[i]
            prm_prdct_lst.append(prdct)
        
        # print(f'{len(prm_array_r)} = {len(prm_prdct_lst)}???')
        
        prm_array = np.reshape(np.asarray(prm_prdct_lst), (32,32))
        
        print('Image Prime Array: ',prm_array.shape)
        print('Image Prime Array First Row:\n', prm_array[0])
        
        
    if sys.argv[1] == 'transform_img_batch':
        fn = r'/home/carl1/projects/cifar-10-batches-py/data_batch_1'
        
        num_images = input('How many images would you like to transform? ')
            
        dct_transformed = rgb2prm(fn, int(num_images))
            
        print(dct_transformed)
        


        
        


