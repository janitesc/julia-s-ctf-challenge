#!/bin/bash
set -ex  # -x so you can see exactly what runs

cd /challenge

if ! ls memdump.* >/dev/null 2>&1; then
    echo "start.sh: running the evil trojan horse"
    python3 malicious.py
else 
    echo "start.sh: memdump already exists, skipping malicious.py"
fi

echo "start.sh: done generating memdump, exiting."