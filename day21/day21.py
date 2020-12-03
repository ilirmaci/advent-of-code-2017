#!/usr/bin/env python3

from typing import Tuple, Iterator, Sequence

Pattern = Tuple[str, ...]
Rule = Tuple[Pattern, Pattern]
Slice = Tuple[int, int]


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


def all_versions(pat: Pattern) -> Iterator[Pattern]:
    '''
    Yield all different equivalent transformations of `pat`
    '''
    current = pat
    for _ in range(4):
        yield(current)
        yield(flip_hor(current))
        current = rotate_left(current)


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
    raise KeyError(f'Could not find any rules for {pat}')


def count_pixels(pat: Pattern) -> int:
    '''
    Return the number of pixels that are on in `pat`
    '''
    result = 0
    for row in pat:
        result += sum(1 for _ in row if _ == '#')
    return result


def slice_pattern(pat: Pattern, row_slice: Slice, col_slice: Slice) -> Pattern:
    '''
    Return 2-d slice of `pat`.
    '''
    rstart, rend = row_slice
    cstart, cend = col_slice
    return tuple(r[cstart:cend] for r in pat[rstart:rend])


def split_n(pat: Pattern, n: int) -> Sequence[Pattern]:
    '''
    Return all sub-paterns of size `n` from splitting `pat`.
    The results are sorted row-wise.
    '''
    size = len(pat)
    slices = [(start, start+n) for start in range(0, size, n)]
    idx = ((r_slice, c_slice) for r_slice in slices for c_slice in slices)
    return tuple(slice_pattern(pat, rs, cs) for rs, cs in idx)


def split(pat: Pattern) -> Sequence[Pattern]:
    '''
    Return `pat` split by 2 if its size is divisible by 2,
    and split by 3 otherwise.
    '''
    size = len(pat)
    if size % 2 == 0:
        return split_n(pat, 2)
    return split_n(pat, 3)


def stitch(pats: Sequence[Pattern]) -> Pattern:
    '''
    Stitch together `pats`. Inverse function of `split`.
    '''
    size = len(pats)
    row_length = int(size**.5)
    result = tuple()
    for start in range(0, size, row_length):
        end = start + row_length
        rows = tuple(sum(cols, start=()) for cols in zip(*pats[start:end]))
        result += rows
    return result


def iterate(pat: Pattern) -> Pattern:
    '''
    Return the result of `split` -> `expand` -> `stitch` for `pat`
    '''
    return stitch([expand(_) for _ in split(pat)])


def iterate_many(pat: Pattern, n: int) -> Pattern:
    current = pat
    for _ in range(n):
        current = iterate(current)
    return current


raw_input = open('day21_input.txt').readlines()
rules = dict(parse_rule(_) for _ in raw_input)

start_str = '.#./..#/###'
start = parse_pattern(start_str)

answer1 = count_pixels(iterate_many(start, 5))
print(f'The answer to the first puzzle is {answer1}')

answer2 = count_pixels(iterate_many(start, 18))
print(f'The answer to the second puzzle is {answer2}')
