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
        self.p = values_dict['p']
        self.v = values_dict['v']
        self.a = values_dict['a']

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
        result_a = sum(abs(_) for _ in self.a)
        result_v = sum(abs(_) for _ in self.v)
        result_p = sum(abs(_) for _ in self.p)
        return (result_a, result_v, result_p)

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
