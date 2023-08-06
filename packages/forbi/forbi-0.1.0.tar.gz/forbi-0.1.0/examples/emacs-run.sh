#!/bin/sh

# This script opens new messages in a new Emacs buffer. This only
# works if you have Emacs running as a server. This can be done by
# adding (server-start) to your .emacs file.

from="$1"
to="$2"
msg="$3"
filename="/tmp/forbi-msg"

echo -n "$from says:\n\n$msg" > "$filename"
emacsclient -n "$filename" 2>/dev/null
