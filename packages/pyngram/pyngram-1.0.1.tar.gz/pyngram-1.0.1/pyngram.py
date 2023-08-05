#!/usr/bin/env python
"""
 A simple Python n-gram calculator. 

 Given an arbitrary string, and the value of n as the size of the n-gram (int), this module 
 will show you the results, sorted from most to least frequently occuring n-gram.

 The 'sort by value' operation for the dict follows the PEP 265 recommendation.

 Quick start:

 >>> from pyngram import calc_ngram

 method expects inputstring as 1st arg, size of n-gram as 2nd arg

 >>> calc_ngram('bubble bobble, bubble bobble, bubble bobble', 3)

 Or just run it from the command line prompt: 
 user@host:~$ ./pyngram.py

 Enjoy!

 Jay Liew
 @jaysern

"""

__version__ = '1.0'
__author__ = 'Jay Liew' # @jaysern from @websenselabs
__license__ = 'MIT'

from operator import itemgetter

def calc_ngram(inputstring, nlen):
    if nlen < 1:
        raise ValueError,"""Uh, n-grams have to be of size 1 or greater. 
(doesn't make much sense otherwise)"""

    if len(inputstring) < 1:
        raise ValueError, """umm yeah, ... the inputstring has to be longer than 1 char ;)"""

    # now, fish out the n-grams from the input string
    # note: a string of length l will have (l-n+1) n-grams of length n
    ngram_list = [inputstring[x:x+nlen] for x in xrange(len(inputstring)-nlen+1)]

    ngram_freq = {} # dict for storing results

    for n in ngram_list: # collect the distinct n-grams and count
        if n in ngram_freq:
            ngram_freq[n] += 1 
        else:
            ngram_freq[n] = 1 # human counting numbers start at 1

    # set reverse = False to change order of sort (ascending/descending)
    return sorted(ngram_freq.iteritems(), key=itemgetter(1), reverse=True)

if __name__ == '__main__':
    inputstring = raw_input('Enter input string: ')
    nlen_str = raw_input('Enter size of n-gram (int): ')
    nlen = int(nlen_str) # cast string to int
    
    for t in calc_ngram(inputstring, nlen):
        print t[0] + ' occured ' + str(t[1]) + ' times'
