#!/usr/bin/env python

# script to answer questions from http://adventofcode.com/2017/day/17

from __future__ import print_function

def next_position(position, buffer_size, steps):
    '''(int, int, int) => int
    Return the next position of the cursor given current `position`,
    the current buffer length, and the number of steps to advance.
    '''
    return ((position + step) % buffer_size) + 1

def make_inserts(num_inserts, steps):
    '''() => list of int
    Return a buffer after `num_inserts` updates advancing `steps` each time.
    '''
    result = [0]
    pos = 1
    
    # value to be inserted doubles as buffer size before insertion
    for current_value in xrange(1, num_inserts + 1):
        pos = next_position(pos, current_value, steps)
        result.insert(pos, current_value)
    return result

if __name__ == '__main__':
    
    steps = 366       ## puzzle input
    
    ####################
    ##  First puzzle  ##
    ####################
    
    qq = make_inserts(2017, steps)
    idx_2017 = qq.index(2017)                            ## where is 2017?
    idx_next = (idx_2017 + 1) if idx_2017 < 2017 else 1  ## avoid IndexError
    first_solution = qq[idx_next]
    print('The answer to the first puzzle is {}'.format(first_solution))
    
    #####################
    ##  Second puzzle  ##
    #####################
    
    # second index will never be displaced by others
    # no need to do the inserts
    
    pos = 1            ## reset position
    
    for buffer_size in xrange(1, 50000001):
        pos = next_position(pos, buffer_size, steps)        
        # only need to record inserts that would go to 2nd position
        if pos == 1: 
            second_solution = buffer_size
    
    print('The answer to the second puzzle is {}'.format(second_solution))

