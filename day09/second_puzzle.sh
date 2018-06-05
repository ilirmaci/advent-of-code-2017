#!/usr/bin/env bash

cat day09_input.txt |       ## read file
    sed 's/\!.//g' |        ## remove all cancelled characters
    grep -Eo '<[^>]*>' |    ## put garbage in own line
    awk '{tot += length($0) - 2}; END {print tot}'  ## get sum
