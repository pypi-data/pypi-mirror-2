# A simple Python n-gram calculator.
#
# Given an arbitrary string, and the value of n as the size of the 
# n-gram (int), this module will show you the results, sorted from 
# most to least frequently occuring n-gram.
#
# The 'sort by value' operation for the dict follows the 
# PEP 265 recommendation.
#
# Installation: 
#
# user@host:~$ sudo pip install pyngram
#
# Quick start:
#
# >>> from pyngram import calc_ngram
#
# method expects inputstring as 1st arg, size of n-gram as 2nd arg
#
# >>> calc_ngram('bubble bobble, bubble bobble, bubble bobble', 3)
#
# or straight from your *nix shell prompt
#
# user@host:~$ ./pyngram.py
# 
# Enjoy!
#
# Jay Liew 
# @jaysern
#
