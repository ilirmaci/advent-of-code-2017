#!/usr/bin/env bash

target=day09_input_no_garbage.txt

cat day09_input.txt |             ## read file
    sed 's/\!.//g' |              ## remove all cancelled characters
    sed 's/<[^>]*>//g' > $target  ## remove garbage and save
