#!/bin/sh

# This script opens new messages in an xmessage window and makes a
# sine wave at the same time.

from="$1"
to="$2"
msg="$3"

speaker-test -t sine >/dev/null 2>&1 &
xmessage -center "$from says: $msg"
pkill speaker-test
