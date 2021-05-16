#!/bin/bash

input_file="$( pwd )/$1"
output_file="$( pwd )/${2:-output.mp3}"
beat_shift="${3:-2}"

wd="$( pwd )"
ls="$( ls )"

mono_file="mono.wav"
shifted_file="shifted.wav"
temp_output_file="temp_output.mp3"

bpm="$( sox $input_file -t raw -r 44100 -e float -c 1 - | bpm )"
delay="$(awk "BEGIN {printf \"%.4f\", $beat_shift * 60 / $bpm}")"

sox $input_file $mono_file channels 1
sox $mono_file $shifted_file pad $delay
sox -M $mono_file $shifted_file $temp_output_file remix -m 1 2

rm $mono_file
rm $shifted_file

# TODO: Copy id3 tags from input_file to temp_output_file

mv $temp_output_file $output_file
