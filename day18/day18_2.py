#!/usr/bin/env python

# Solutions to the second puzzle of day 18 http://adventofcode.com/2017/day/18

from __future__ import print_function
from collections import deque         ## efficient queue
from day18_1 import parse_instruction, get_val, set_, add, mul, mod, jgz

# redefine functions that have taken a new meaning
def snd(arg, register, queue):
    '''(str, dict of str:int, deque of int) => NoneType
    Add the value of `arg` to the start of the `queue`.
    '''
    queue.appendleft(get_val(arg, register))

def rcv(arg, register, queue):
    '''(str, dict of str:int, deque of int) => NoneType
    Consume the next value in `queue` and assign it to `register[arg]`.
    '''
    register[arg] = queue.pop()

def is_stuck(instr, queue):
    '''(str, deque) => bool
    Return True if both `instr` ask to receive and the queue is empty.
    '''
    return (instr == 'rcv') and (len(queue) == 0)

if __name__ == '__main__':
    # read input    
    input_raw = open('day18_input.txt').readlines()
    instr = [parse_instruction(x) for x in input_raw]

    # define dictionary with the instructions that don't return anything
    cmd2func = {'set':set_, 'add':add, 'mul':mul, 'mod':mod}

    # start state variables for both programs
    idx = [0, 0]                            ## instructions index
    stuck = [False, False]                  ## status
    register = [{'p':x} for x in range(2)]  ## register of values
    queue = [deque(), deque()]              ## queue of values sent to program
    sent = [0, 0]                           ## number of values sent by program
    num_instructions = len(instr)           

    while (not all(stuck)):
        for prog in range(2):
            ii = idx[prog]
            instruction, arguments = instr[ii]
            other_prog = 1 - prog
            stuck[prog] = is_stuck(instruction, queue[prog])
            
            # don't process program's instructions if it's stuck or terminated
            if stuck[prog] or (ii < 0) or (ii >= num_instructions):
                continue
            
            #print(prog, ii + 1, instr[ii], queue[prog])  ## debug
            if instruction in cmd2func:
                cmd2func[instruction](arguments, register[prog], None)
                ii += 1
            elif instruction == 'snd':
                snd(arguments[0], register[prog], queue[other_prog])
                ii += 1
                sent[prog] += 1
            elif instruction == 'rcv':
                rcv(arguments[0], register[prog], queue[prog])
                ii += 1
            elif instruction == 'jgz':
                ii += jgz(arguments, register[prog])
            else:
                raise NameError('Unknown instruction {}'.format(instruction))
            idx[prog] = ii
    
    second_solution = sent[1]
    print('The solution to the second puzzle is {}'.format(second_solution))

