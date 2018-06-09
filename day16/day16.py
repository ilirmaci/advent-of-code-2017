#!/usr/bin/env python

# Solutions to day 16 puzzles http://adventofcode.com/2017/day/16

from __future__ import print_function

# define operations as functions that take a list of arguments
# and change the list in place to save copies
def spin(args, pos):
    x = int(args[0])
    pos[:] = pos[-x:] + pos[:-x]

def exchange(args, pos):
    a, b = (int(x) for x in args)
    pos[a], pos[b] = pos[b], pos[a]

def partner(args, pos):
    idxa, idxb = (pos.index(x) for x in args)
    pos[idxb], pos[idxa] = pos[idxa], pos[idxb]

def apply_commands(commands, pos, function_map=instruction2func):
    '''(list of str, list of str, dict of str:function) => NoneType
    Modify `pos` in place applying `commands` in order.
    '''
    for command in commands:
        instruction = command[0]
        args = command[1:].split('/')
        instruction2func[instruction](args, pos)

if __name__ == '__main__':
    input_raw = open('day16/day16_input.txt').readlines()
    input_split = input_raw[0].split(',')
    initial_positions = list('abcdefghijklmnop')
    
    # place the functions in a dictionary for quick conversion
    instruction2func = {'s':spin, 'x':exchange, 'p':partner}
    
    ####################
    ##  First puzzle  ##
    ####################
    
    pos = initial_positions[:]   ## deep copy
    apply_commands(input_split, pos, instruction2func)
    print('The solution to the first puzzle is {}'.format(''.join(pos)))
    
    #####################
    ##  Second puzzle  ##
    #####################
    
    pos2 = initial_positions[:]  ## reset
      
    # see how many iterations it takes to come back to first positions
    apply_commands(input_split, pos2, instruction2func)   ## run once
    count = 1

    while pos2 != initial_positions:
        apply_commands(input_split, pos2, instruction2func)
        count += 1
        
    # we can avoid running transforming any multiple of count
    num_transformations = 1000000000 % count

    # we only need to run commands num_transformations times
    for _ in range(num_transformations):
        apply_commands(input_split, pos2, instruction2func)

    print('The solution to the second puzzle is {}'.format(''.join(pos2)))

