#!/bin/bash

# Your Python script code goes here

# Get current date and format it as "dayth Month" (e.g., 3th Oct)
current_date=$(date +"%dS %b")

# After your script finishes running, add, commit, and push
git add .
git commit -m "Update on ${current_date}"
git push
