#!/usr/bin/env python3

from typing import Tuple, Iterator

Pattern = Tuple[str, ...]
Rule = Tuple[Pattern, Pattern]


def parse_pattern(string: str) -> Pattern:
    '''
    Return pattern from `string`
    '''
    rows = string.split('/')
    return tuple([tuple(row) for row in rows])


def print_pattern(pat: Pattern):
    for row in pat:
        print(''.join(row))


def parse_rule(line: str) -> Rule:
    '''
    Return rule described in `line`
    '''
    in_, out_ = line.strip().split(' => ')
    return parse_pattern(in_), parse_pattern(out_)


def rotate_left(pat: Pattern) -> Pattern:
    size = len(pat)
    result = []
    for input_col in reversed(range(size)):
        result.append(tuple(pat[_][input_col] for _ in range(size)))
    return tuple(result)


def flip_hor(pat: Pattern) -> Pattern:
    return tuple(reversed(pat))


def flip_ver(pat: Pattern) -> Pattern:
    return tuple([tuple(reversed(row)) for row in pat])


def all_versions(pat: Pattern) -> Iterator[Pattern]:
    '''
    Yield all different equivalent transformations of `pat`
    '''
    current = pat
    for _ in range(4):
        yield(current)
        current = rotate_left(current)
    yield(flip_hor(pat))
    yield(flip_ver(pat))


def expand(pat: Pattern) -> Pattern:
    '''
    Return expansion of `pat` based on `rules`. Try to find a version that
    is in the rules.
    '''
    for pat_version in all_versions(pat):
        try:
            return rules[pat_version]
        except KeyError:
            continue
    raise KeyError('Could not find any rules for {}', pat)


def count_pixels(pat: Pattern) -> int:
    '''
    Return the number of pixels that are on in `pat`
    '''
    result = 0
    for row in pat:
        result += len([_ for _ in row if _ == '#'])
    return result


raw_input = open('day21_input.txt').readlines()
rules = dict(parse_rule(_) for _ in raw_input)

start_str = '.#./..#/###'
start = parse_pattern(start_str)
