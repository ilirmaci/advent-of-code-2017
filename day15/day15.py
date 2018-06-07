#!/usr/bin/env python

# python script to answer questions from http://adventofcode.com/2017/day/15

# lazily evaluated zip and infinite generator limiter
from itertools import izip, islice
from __future__ import print_function

# puzzle inputs
inputA = 679
inputB = 771

# test inputs
testA = 65
testB = 8921

def gen(start, factor):
    '''(int, int) => generator of int
    Yield sequence of generator defined by `factor` and starting with `start`
    '''
    val = start
    while True:
        val = (val * factor) % 2147483647
        yield val

def judge_equal(tpl):
    '''(tuple of (int, int)) => bool
    Return True if the last 16 bits of `tpl` entries are equal
    '''
    a, b = tpl
    return (a % 2**16) == (b % 2**16)


def start_generators(startA, startB):
    '''(int, int) => generator of (int, int)
    Start both generators and return an interable of values from each one (a, b)
    '''
    genA = gen(startA, 16807)
    genB = gen(startB, 48271)
    return (x for x in izip(genA, genB))

# test generators
test_gens = start_generators(testA, testB)

# get first 5 values of each
for _ in range(5):
    print(next(test_gens))
    
# event better, use and explicit iterator
for x in islice(test_gens, 5):
    print(x)


# restart test generators and get count of matches, expected 588
test_gens = start_generators(testA, testB)
sum((judge_equal(p) for p in islice(test_gens, 40000000)))

####################
##  First puzzle  ##
####################

gens = start_generators(inputA, inputB)
first_solution = sum((judge_equal(p) for p in islice(gens, 40000000)))
print('The answer to the first puzzle is {}'.format(first_solution))

#####################
##  Second puzzle  ##
#####################

# we need to redefine the procedure for starting the generators
def start_generators_filtered(startA, startB, critA, critB):
    '''(int, int, int, int) => generator of (int, int)
    Start both generators, apply the  and return an interable of values from each one (a, b)
    '''
    genA = gen(startA, 16807)
    genA_filter = (x for x in genA if x % critA == 0)
    
    genB = gen(startB, 48271)
    genB_filter = (x for x in genB if x % critB == 0)
    
    return (x for x in izip(genA_filter, genB_filter))


# start generators with filtering
gens_filter_test = start_generators_filtered(testA, testB, 4, 8)

# try the first few entries
for x in islice(gens_filter_test, 5):
    print(x)

# start proper generators
gens_filter = start_generators_filtered(inputA, inputB, 4, 8)
second_solution = sum((judge_equal(p) for p in islice(gens_filter, 5000000)))
print('The answer to the second puzzle is {}'.format(second_solution))
