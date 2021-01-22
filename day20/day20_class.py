#!/usr/bin/env python

# Class and functions needed for http://adventofcode.com/2017/day/20


def values(input_string):
    '''Parse values from input string of a single attribute'''
    input_string = input_string.strip()
    var = input_string[0]
    vals = tuple(int(x) for x in input_string[3:-1].split(','))
    return var, vals


class Part(object):
    '''Particle object'''

    def __init__(self, index, raw_string):
        line = raw_string.strip()
        values_dict = dict([values(x) for x in line.split(', ')])
        self.id = index
        # organize by dimension, s of (a, v, p)
        self.a = values_dict['a']
        self.v = values_dict['v']
        self.p = values_dict['p']
        self.avp = (self.a, self.v, self.p)

    # organize by measurement, tuples of (x, y, z)
    def xyz(self):
        x = (self.a[0], self.v[0], self.p[0])
        y = (self.a[1], self.v[1], self.p[1])
        z = (self.a[2], self.v[2], self.p[2])
        return (x, y, z)

    def update(self):
        '''Update velocity and position advancing time by one unit'''
        self.v = tuple(v + a for v, a in zip(self.v, self.a))
        self.p = tuple(p + v for p, v in zip(self.p, self.v))

    def update_n(self, n):
        '''Update velocity and position advancing time by `n` units'''
        self.v = tuple(v + n*a for v, a in zip(self.v, self.a))
        pva = zip(self.p, self.v, self.a)
        self.p = tuple(p + n*v + n*(n+1)*a/2 for p, v, a in pva)

    def distance(self, other):
        '''Return L1 distance from `other` particle'''
        return sum([abs(x - y) for x, y in zip(self.p, other.p)])

    def key(self):
        '''Return a 3-tuple that can be used to sort particles
        so that the ones ending up closest to the origin come first
        '''
        result = tuple(sum(abs(_) for _ in mag) for mag in self.avp)
        return result

    def direction(self, dim):
        '''Return -1 if all magnitudes (acceleration, velocity, position)
        for dimension `dim` are on the negative side of the origin,
        +1 if they are all on the positive side, and 0 if they are not
        pointing in the same direction.
        '''
        current_dim = self.xyz()[dim]
        if (min(current_dim) <= 0) and (max(current_dim) <= 0):
            return -1
        if (min(current_dim) >= 0) and (max(current_dim) >= 0):
            return 1
        return 0

    def can_collide(self, other):
        '''Return True if collision with `other` is still possible'''
        # if particles are definitely diverging on any dimension
        # return False
        for dim in range(3):
            p, v, a = self.p[dim], self.v[dim], self.a[dim]
            op, ov, oa = other.p[dim], other.v[dim], other.a[dim]
            if (p > op) and (v > ov) and (a > oa):
                return False
            elif (p < op) and (v < ov) and (a < oa):
                return False
        return True
