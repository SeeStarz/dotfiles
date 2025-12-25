#!/bin/bash
# Usage: ./rclone_bisync_log.sh <logfile> <rclone arguments>

LOGFILE="$1"
shift

# Run the rclone command, remove excess newlines, append to log
rclone bisync "$@" 2>&1 | sed -z 's/\n*$/\n/' >> "$LOGFILE"
EXIT_STATUS=${PIPESTATUS[0]}

# Append date and result
DATE=$(date '+%Y/%m/%d %H:%M:%S')
if [ $EXIT_STATUS -eq 0 ]; then
    echo "$DATE SUCCESS: Sync completed" >> "$LOGFILE"
else
    echo "$DATE ERROR: rclone bisync failed with exit code $EXIT_STATUS" >> "$LOGFILE"
fi
