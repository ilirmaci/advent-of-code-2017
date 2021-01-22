#!/usr/bin/env python

# Class and functions needed for http://adventofcode.com/2017/day/20

def values(input_string):
    '''Parse values from input string of a single attribute'''
    input_string = input_string.strip()
    var = input_string[0]
    vals = [int(x) for x in input_string[3:-1].split(',')]
    return var, vals

class Part(object):
    '''Particle object'''

    def __init__(self, index, raw_string):
        line = raw_string.strip()
        values_dict = dict([values(x) for x in line.split(', ')])
        self.id = index
        self.pos = values_dict['p']
        self.vel = values_dict['v']
        self.acc = values_dict['a']
    
    def update(self):
        '''Update velocity and position advancing time by one unit'''
        self.vel = [v + a for v,a in zip(self.vel, self.acc)] 
        self.pos = [p + v for p,v in zip(self.pos, self.vel)]
    
    def update_n(self, n):
        '''Update velocity and position advancing time by `n` units'''
        self.vel = [v + n*a for v,a in zip(self.vel, self.acc)]
        self.pos = [p + n*v + n*(n+1)*a/2 for p, v, a in zip(self.pos, self.vel, self.acc)]
    
    def distance(self, other):
        '''Return L1 distance from `other` particle'''
        return sum([abs(x - y) for x, y in zip(self.pos, other.pos)])
    
    def can_collide(self, other):
        '''Return True if collision with `other` is still possible'''
        # if particles are definitely diverging on any dimension
        # return False
        for dim in range(3):
            if (self.acc[dim] > other.acc[dim]) and (self.vel[dim] > other.vel[dim]) and (self.pos[dim] > other.pos[dim]):
                return False
            elif (self.acc[dim] < other.acc[dim]) and (self.vel[dim] < other.vel[dim]) and (self.pos[dim] < other.pos[dim]):
                return False
        return True
