#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <room_name> <video_socket_path> <audio_socket_path>"
  exit 1
fi

command="./livekit-cli"
url="wss://myapp-f7yiyst6.livekit.cloud"
api_key="APIFmHdCZn5S3vC"
api_secret="9o0FmgOGNkynrJzDrySBNol8BNVnO0k24UvUEy2VAsN"
room=$1
video_sock=$2
audio_sock=$3

"$command" join-room --identity bot --url "$url" --api-key "$api_key" --api-secret "$api_secret" --room "$room" --publish "h264://$video_sock" --publish "opus://$audio_sock"

