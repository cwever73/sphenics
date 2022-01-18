#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 09:40:25 2022

@author: carl
"""

import itertools
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
        


