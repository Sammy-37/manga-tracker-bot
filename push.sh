#!/bin/bash

# 1. Add all changes
git add .

# 2. Commit with a timestamp if no message is provided
if [ -z "$1" ]; then
    msg="Auto-update: $(date)"
else
    msg="$1"
fi

git commit -m "$msg"

# 3. Push to GitHub
git push origin main

echo "✅ Successfully pushed to GitHub!"
