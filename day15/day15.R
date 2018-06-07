#!/usr/bin/env R

# R script to answer questions from http://adventofcode.com/2017/day/15

# puzzle inputs
inputA <- 679
inputB <- 771

# test inputs
testA <- 65
testB <- 8921

# constructor function for generators
build_generator <- function(fctr) {
    # return function that multiplies input by `fctr`
    # and takes the remainder from dividing it with magic constant
    function(x) (x * fctr) %% 2147483647
}

# comparison function between two values
judge_equal <- function(x, y) (x %% 2^16) == (y %% 2^16)

# function to count agreements between two generators
num_agreements <- function(genA, genB, startA, startB, sample_size) {
    # Return count of agreements when drawing `sample_size` outputs from
    # `genA` and `genB`.
    
    a <- startA; b <- startB
    result = 0
    
    for (ii in 1:sample_size) {
    a <- genA(a); b <- genB(b)
    if (judge_equal(a, b)) result <- result + 1
    }
    
    return(result)
}

####################
##  First puzzle  ##
####################

# create generators
genA <- build_generator(16807)
genB <- build_generator(48271)

# test a single value
genA(testA)        ## 1092455
genB(genB(testB))  ## 1233683848

# test solution, expected result 588
num_agreements(genA, genB, testA, testB, sample_size=4e7)

first_solution <- num_agreements(genA, genB, inputA, inputB, sample_size=4e7)
print(paste('The solution to the first puzzle is', first_solution))


#####################
##  Second puzzle  ##
#####################

# constructor that adds filtering to a generator
# all functional-like!
add_filter <- function(gen, criterion) {
    # Return a function that calls `gen` until output is 
    # divisible by `criterion`
    
    function(x) {
        candidate = gen(x)
        if (candidate %% criterion == 0) return(candidate)
        return(add_filter(gen, criterion)(candidate))
    }
}

# add filter to generators
genAfilter <- add_filter(genA, 4)
genBfilter <- add_filter(genB, 8)

# try a few values
genAfilter(genAfilter(testA))  ## 1992081072
genBfilter(testB)              ## 1233683848

second_solution <- num_agreements(genAfilter, genBfilter, inputA, inputB, 5e6)
print(paste('The solution to the second puzzle is', second_solution))

