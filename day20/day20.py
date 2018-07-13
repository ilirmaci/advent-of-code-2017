#!/usr/bin/env python

# Solutions to day 20 puzzles http://adventofcode.com/2017/day/20

from __future__ import print_function
from day20_class import Part

# read input
raw_input = open('day20_input.txt').readlines()
particles = [Part(ii, raw_input[ii]) for ii in xrange(len(raw_input))]

####################
##  First puzzle  ##
####################

# hacky solution that relies on some particles having no acceleration
def no_acc(particle):
    '''(Part) => bool
    Return True if acceleration across all dimensions is 0, False otherwise.
    '''
    return sum([abs(x) for x in particle.acc]) == 0

candidates = [pp for pp in particles if no_acc(pp)]
candidate_velocities = [sum([abs(x) for x in pp.vel]) for pp in candidates]

# which candidate has the smallest velocity
smallest_index = candidate_velocities.index(min(candidate_velocities))
first_solution = candidates[smallest_index].id
print('The answer to the first puzzle is {}'.format(first_solution))

#####################
##  Second puzzle  ##
#####################


second_solution = 'still nothing'
print('The answer to the second puzzle is {}'.format(second_solution))

