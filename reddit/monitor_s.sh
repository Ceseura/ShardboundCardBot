#!/bin/bash
until python redditBot.py submissions; do
    echo "script crashed with exit code $?. Restarting..." >&2
    sleep 1
done
