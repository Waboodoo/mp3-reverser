#!/bin/bash
# set -x

temp_output_file="temp_output.mp3"

# Argument handling

input_file="$( pwd )/$1"
output_file="$( pwd )/$2"
shift
shift

reverse=false
beat_shift="0"
keep_pitch=false
speed="1"

while test $# -gt 0; do
  case "$1" in
    --reverse)
      shift
      reverse=true
      ;;
    --keep-pitch)
      shift
      keep_pitch=true
      ;;
    --speed)
      shift
      if [[ $# -gt 0 ]]
      then
        speed="$1"
        shift
      else
        echo "no speed parameter specified"
        exit 1
      fi
      ;;
    --stereo-shift)
      shift
      if [[ $# -gt 0 ]]
      then
        beat_shift="$1"
        shift
      else
        echo "no beat shift parameter specified"
        exit 1
      fi
      ;;
    *)
      break
      ;;
  esac
done

# File Processing

# REVERSE
if $reverse
then
  temp_output_file="temp_reverse_output.mp3"
  sox $input_file $temp_output_file 'reverse'
  input_file="$temp_output_file"
fi

# CHANGE SPEED
if [[ $speed != "1" ]]
then
  temp_output_file="temp_speed_output.mp3"

  if $keep_pitch
  then
    sox $input_file $temp_output_file 'tempo' $speed
  else
    sox $input_file $temp_output_file 'speed' $speed
  fi
  input_file="$temp_output_file"
fi

# BEAT SHIFT
if (( beat_shift != "0" ))
then
  temp_output_file="temp_beat_shift_output.mp3"

  mono_file="mono.wav"
  shifted_file="shifted.wav"

  bpm="$( sox $input_file -t raw -r 44100 -e float -c 1 - | bpm )"
  delay="$(awk "BEGIN {printf \"%.4f\", $beat_shift * 60 / $bpm}")"

  sox $input_file $mono_file channels 1
  sox $mono_file $shifted_file pad $delay
  sox -M $mono_file $shifted_file $temp_output_file remix -m 1 2

  rm $mono_file
  rm $shifted_file
  input_file="$temp_output_file"
fi

# Finalizing
# TODO: Copy id3 tags from input_file to temp_output_file
mv $temp_output_file $output_file
