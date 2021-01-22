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


def same_order(a, b):
    '''Return True if elements in `a` appear in the same order as in `b`
    '''
    return a == [_ for _ in b if _ in a]


def can_collide_1d(particles, dim, final_order):
    '''Return True if collisions are still possible in given dimension
    '''
    # check that all magnitudes (acceleration, velocity, position)
    # point in different directions. If they do collisions can still happen
    different_directions = [_.id for _ in particles if _.direction(dim) == 0]
    if len(different_directions) > 0:
        return True
    # sort particles in the same direction by position
    pos = [_ for _ in particles if _.direction(dim) > 0]
    pos_sorted = [_.id for _ in sorted(pos, key=lambda x: x.p[dim])]
    neg = [_ for _ in particles if _.direction(dim) < 0]
    neg_sorted = [_.id for _ in sorted(neg, key=lambda x: x.p[dim])]
    pos_in_same_order = same_order(pos_sorted, final_order[dim])
    neg_in_same_order = same_order(neg_sorted, final_order[dim])
    return pos_in_same_order and neg_in_same_order


def can_collide(particles, final_order):
    '''Return True if collisions among `particles` are still possible.
    '''
    for dim in range(3):
        if not can_collide_1d(particles, dim, final_order):
            return False
    return True


# get final order of particles (in distance from origin)
# along each dimension
final_ord = []
for dim in range(3):
    sorted_particles = sorted(particles, key=lambda x: x.xyz()[dim])
    final_ord.append([_.id for _ in sorted_particles])

while can_collide(particles, final_ord):
    particles = remove_collisions(particles)
    for particle in particles:
        particle.update()

second_solution = len(particles)
print('The answer to the second puzzle is {}'.format(second_solution))
