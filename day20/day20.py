#!/usr/bin/env python

# Solutions to day 20 puzzles http://adventofcode.com/2017/day/20

from __future__ import print_function
from day20_class import Part

# read input
raw_input = open('day20_input.txt').readlines()
particles = [Part(ii, raw_input[ii]) for ii in range(len(raw_input))]

##################
#  First puzzle  #
##################

closest_particle = sorted(particles, key=lambda x: x.key())[0]
print('The answer to the first puzzle is {}'.format(closest_particle.id))

###################
#  Second puzzle  #
###################


def remove_collisions(particles):
    '''Return `particles` with the colliding particles removed.
    '''
    # make a summary of all positions and their frequency
    count = {}
    for _ in particles:
        count[_.p] = count.get(_.p, 0) + 1
    # only return particles with frequency == 1
    return [_ for _ in particles if count[_.p] == 1]


second_solution = 'still nothing'
print('The answer to the second puzzle is {}'.format(second_solution))
