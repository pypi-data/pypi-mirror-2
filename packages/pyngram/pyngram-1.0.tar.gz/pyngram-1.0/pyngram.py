#!/usr/bin/env python

# A simple Python n-gram calculator. 
#
# Given an arbitrary string, and the value of n as the size of the n-gram (int), this code 
# snip will show you the results, sorted from most to least frequently occuring n-gram.
#
# The 'sort by value' operation for the dict follows the PEP 265 recommendation.
#
# Quick start:
#
# from pyngram import calc_ngram
# calc_ngram('bubble bobble, bubble bobble, bubble bobble', 3) # 3 here is the size of the n-gram
#
# Or just run it from the command line prompt: 
# bash> python pyngram.py
#
# Enjoy!
#
# - Jay Liew

__version__ = '1.0'
__author__ = 'Jay Liew' # @jaysern from @websenselabs
__license__ = 'MIT'

from operator import itemgetter

def calc_ngram(inputstring, nlen):
    if nlen < 1:
        print "Uh, n-grams have to be of size 1 or greater. (doesn't make much sense otherwise)"
        sys.exit(-1)

    if len(inputstring) < 1:
        print "umm yeah, ... the inputstring has to be longer than 1 char ;)"
        sys.exit(-1)

    # now, fish out the n-grams from the input string
    ngram_list = [inputstring[x:x+nlen] for x in xrange(len(inputstring))]

    ngram_freq = {} # dict for storing results

    for n in ngram_list: # collect the distinct n-grams and count
        if len(n) == nlen:
            if n in ngram_freq:
                ngram_freq[n] += 1 
            else:
                ngram_freq[n] = 1 # human counting numbers start at 1
        else:
            # these are the remainder strings not long enough to fit n
            pass

    # set reverse = False to change order of sort (ascending/descending)
    return sorted(ngram_freq.iteritems(), key=itemgetter(1), reverse=True)

if __name__ == '__main__':
    inputstring = raw_input('Enter input string: ')
    nlen_str = raw_input('Enter size of n-gram (int): ')
    nlen = int(nlen_str) # cast string to int
    
    for t in calc_ngram(inputstring, nlen):
        print t[0] + ' occured ' + str(t[1]) + ' times'
