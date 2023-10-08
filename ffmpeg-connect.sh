#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <video_socket_path> <audio_socket_path>"
  exit 1
fi

video_socket="$1"
audio_socket="$2"

ffmpeg \
  -f v4l2 -thread_queue_size 1024 -i /dev/video0 -r 30 \
  -c:v libx264 -bsf:v h264_mp4toannexb -b:v 500k -profile:v main -pix_fmt yuv420p \
  -x264-params keyint=30 -max_delay 0 -bf 0 -f h264 -listen 1 "unix:$video_socket" \
  -f alsa -thread_queue_size 1024 -i hw:0 -sample_rate 44100 -channels 2 -c:a libopus -b:a 64k -page_duration 20000 -vn \
  -f opus -listen 1 "unix:$audio_socket"
