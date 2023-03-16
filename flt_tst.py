#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:41:35 2023

@author: cmwever73

purpose: test out precision that python can store a decimal
"""

from decimal import Decimal
import string
import sys
import traceback


def trnscrb(inpt_txt, plchldr=2):
    '''Given a string, output dict of numeric
    represenation in float and string type'''
    
    #dont care about punctuation
    pnc_lst = string.punctuation + '“”–'
    #lowercase everything
    inpt_txt = inpt_txt.casefold()
    
   
    trnslt_dct = {lttr: '0'*(plchldr - len(str(indx))) + str(indx) \
                  for indx, lttr in enumerate(string.ascii_lowercase, 1)}
    
    #account for spaces
    trnslt_dct[' '] = '00'
    
    print(trnslt_dct)
    
    dcml_dct = {}
    str_int = '0.'
    
    for i, chrctr in enumerate(inpt_txt):
        if chrctr not in pnc_lst and chrctr != '\n':
            try:
                str_int += trnslt_dct[chrctr]
            except Exception:
                print(traceback.format_exc())
                
        '''Actually, if you use Decimal, dont need this catch below'''        
        #once you get to the end, add so truncation doesnt happen
        # if len(inpt_txt) -1 == i:
            # str_int += '9'*plchldr
            
    
    #create dictionary for comparison sake
    dcml_dct.setdefault(str_int, {})
    dcml_dct[str_int]['float'] = float(str_int)
    dcml_dct[str_int]['float Ratio'] = float(str_int).as_integer_ratio()
    dcml_dct[str_int]['Decimal'] = Decimal(str_int)
    dcml_dct[str_int]['Decimal Ratio'] = Decimal(str_int).as_integer_ratio()
            
    return dcml_dct
            
if __name__ == '__main__':
    
    a = 1.45
    b = 0.008001020999
    print(b.as_integer_ratio())
    #maybe always need to cap with 999 so that there is a definite end
    #ant python doesnt truncate it for you
    dir(float)
    # dir(float.__trunc__())
    #way to turn this 'off'? probably have to override the dunder
    sys.float_info

    
    inpt_txt0 = 'cat in the hat'
    otpt0 = trnscrb(inpt_txt0, 3)
    print(otpt0)
    otpt1 = trnscrb(inpt_txt0)
    print(otpt1)
    
    inpt_txt1 = 'Cat! In the hAt$'
    otpt2 = trnscrb(inpt_txt1)
    print(otpt2)
    
    inpt_txt2 = '''I must not fear. Fear is the mind-killer. 
     Fear is the little-death that brings total obliteration. 
     I will face my fear. I will permit it to pass over me and through me. 
     And when it has gone past I will turn the inner eye to see its path. 
     Where the fear has gone there will be nothing. Only I will remain.'''
     
    otpt3 = trnscrb(inpt_txt2)
    print(otpt3)
    
    #notice that the length of the fraction you get back is bigger than
    #the original message. Is this worth it? Is brefity/smaller storage the
    #point? If so, this isn't worth it. If encryption is (and yo could use a
    #better one and 'decimalize' it) than it might be... dont know. 
    
            
        