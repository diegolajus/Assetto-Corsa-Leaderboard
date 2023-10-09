#!/bin/bash

# Get current date and format it as "dayth Month" (e.g., 3th Oct)
current_date=$(date +"%dth %b")

# After your script finishes running, add, commit, and push
git add .
git commit -m "${current_date}"
git push
