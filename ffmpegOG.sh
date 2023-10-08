ffmpeg -f v4l2 -thread_queue_size 512 -i /dev/video0 -r 30   -c:v libx264 -bsf:v h264_mp4toannexb -b:v 1M -profile:v baseline -pix_fmt yuv420p   -x264-params keyint=120 -max_delay 0 -bf 0   -f h264 -listen 1 unix:/tmp/myvideo.sock   -f alsa -i hw:0   -c:a libopus -page_duration 20000 -vn   -f opus -listen 1 unix:/tmp/myaudio.sock

