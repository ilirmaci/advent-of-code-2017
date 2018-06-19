#!/usr/bin/env python

# Solutions to day 19 puzzles http://adventofcode.com/2017/day/19

from __future__ import print_function

def get_val(coords, grid):
    '''((int, int), list of str) => str
    Return the content of cell (row, col) from `grid`.
    '''
    row, col = coords
    return grid[row][col]

def move(direction, position):
    '''(str, (int, int)) => (int, int)
    Return new coordinates after moving once in `direction` from `position`.
    '''
    row, col = position
    if direction == 'up':
        return (row - 1, col)
    elif direction == 'down':
        return (row + 1, col)
    elif direction == 'left':
        return (row, col - 1)
    elif direction == 'right':
        return (row, col + 1)

def turn(direction, position, grid):
    '''(str, (int, int), list of str) => str
    Get the heading after getting to a crossing in `position` from `direction`.
    '''
    turns[0] += 1
    if direction in ('up', 'down'):
        left_cell = get_val(move('left', position), grid)
        if left_cell == '-':
            return 'left'
        else:
            return 'right'
    else:
        up_cell = get_val(move('up', position), grid)
        if up_cell == '|':
            return 'up'
        else:
            return 'down'

def follow_straight(position, direction, grid):
    '''((int, int), str, list of str) => (int, int)
    Keep moving in `direction` starting from `position` as long as there is
    a path. Return last position of path.
    '''
    while True:
        next_cell = move(direction, position)
        if next_cell != ('-', '|'):
            return position
        position = next_cell

def process_letter(position, direction, visited, grid):
    '''((int, int), str, list of str, list of str) => str
    Add letter at `position` to the end of `visited`. If path continues
    past letter return `direction` otherwise return "stop".
    '''
    visited.append(get_val(position, grid))
    next_cell = get_val(move(direction, position), grid)
    if next_cell != ' ':
        return direction
    return 'stop'

def is_full(position, grid):
    '''((int, int)) => bool
    Return True if `position` is full (path, corner, or letter).
    '''
    return get_val(position, grid) not in (' ', '\n')

def is_crossing(position, grid):
    '''((int, int)) => bool
    Return True if more than one path crosses `position`.
    '''
    this_cell = get_val(position, grid)
    if this_cell == '|':
        left_cell = get_val(move('left', position), grid)
        right_cell = get_val(move('right', position), grid)
        return (left_cell == '-') or (right_cell == '-')
    elif this_cell == '-':
        up_cell = get_val(move('up', position), grid)
        down_cell = get_val(move('down', position), grid)
        return (up_cell == '|') or (down_cell == '|')
    else:
        return False

if __name__ == '__main__':
    # read input
    maze = open('day19_input.txt').readlines()
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    ####################
    ##  First puzzle  ##
    ####################
    
    # start movement from top moving down
    starting_col = maze[0].index('|')
    position = (0, starting_col)
    direction = 'down'
    visited = []
    turns = [0]
    
    while direction != 'stop':
        position = move(direction, position)
        current_cell = get_val(position, maze)
        if current_cell in ('-', '|'):
            position = follow_straight(position, direction, maze)
        elif current_cell == '+':
            direction = turn(direction, position, maze)
        elif current_cell in LETTERS:
            direction = process_letter(position, direction, visited, maze)
    
    first_solution = "".join(visited)
    print('The answer to the first puzzle is {}'.format(first_solution))
    
    #####################
    ##  Second puzzle  ##
    #####################
    
    # generator to iterate over all cell posisions
    cells = ((r, c) for r in xrange(len(maze)) for c in xrange(len(maze[0])))
    
    # the algorithm traverses every full cell once and every crossing twice
    second_solution = sum(is_full(p, maze) + is_crossing(p, maze) for p in cells)
    print('The answer to the second puzzle is {}'.format(second_solution))

