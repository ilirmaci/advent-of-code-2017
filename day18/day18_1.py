#!/usr/bin/env python

# Solutions to the first puzzle of day 18 http://adventofcode.com/2017/day/18

from __future__ import print_function

# parse instructions from line
def parse_instruction(line):
    '''(str) => (str, list of str)
    Return a tuple of (instruction, arguments) from a line.
    '''
    line_split = line.strip().split(' ')
    return (line_split[0], line_split[1:])

# function to evaluate a register or an integer literal (passed as string)
def get_val(x, register):
    '''(str, dict of str:int) => int
    Return `int(x)` if `x` is not a single letter. Otherwise return the
    value from register assigned to `x`. Defaults to 0 if not found. 
    '''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return register.get(x, 0) if x in letters else int(x)

# implement all instructions as functions
# except the last two they all modify arguments in place
# the last two return a value
def snd(args, register, played):
    '''(list of str, dict of str:int, list of str) => NoneType'''
    played[0] = get_val(args[0], register)

def set_(args, register, played):
    '''(list of str, dict of str:int, list of str) => NoneType'''
    x, y = args
    register[x] = get_val(y, register)

def add(args, register, played):
    '''(list of str, dict of str:int, list of str) => NoneType'''
    x, y = args
    register[x] = get_val(x, register) + get_val(y, register)

def mul(args, register, played):
    '''(list of str, dict of str:int, list of str) => NoneType'''
    x, y = args
    register[x] = get_val(x, register) * get_val(y, register)

def mod(args, register, played):
    '''(list of str, dict of str:int, list of str) => NoneType'''
    x, y = args
    register[x] = get_val(x, register) % get_val(y, register)

# these two return something and don't modify
# they don't need to have the same signature as the others
def rcv(args, register):
    '''(list of str, dict of str:int) => bool'''
    x = get_val(args[0], register)
    if x > 0:
        return False
    return True

def jgz(args, register):
    '''(list of str, dict of str:int) => int'''
    x, y = args
    if get_val(x, register) > 0:
        return get_val(y, register)
    return 1

if __name__ == '__main__':
    # read input    
    input_raw = open('day18_input.txt').readlines()
    instr = [parse_instruction(x) for x in input_raw]
    
    # define dictionary with the instructions that don't return anything
    cmd2func = {'snd':snd, 'set':set_, 'add':add, 'mul':mul, 'mod':mod}
    
    # start program by looping over indices
    # stop when rcv returns True or the index goes out of bounds
    idx = 0
    keep_looping = True
    register = dict()
    played = [0]
    num_instructions = len(instr)
    
    while keep_looping and (idx >= 0) and (idx < num_instructions):
        # print(idx + 1, instr[idx], played, get_val('a', register)) ## debug
        instruction, arguments = instr[idx]
        if instruction in cmd2func:
            cmd2func[instruction](arguments, register, played)
            idx += 1
        elif instruction == 'rcv':
            keep_looping = rcv(arguments, register)
            idx += 1
        elif instruction == 'jgz':
            idx += jgz(arguments, register)
        else:
            raise NameError('Unknown instruction {}'.format(instruction))
    
    print(keep_looping)          ## expecting False
    first_solution = played[0]
    print('The solution to the first puzzle is {}'.format(first_solution))

