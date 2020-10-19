#!/bin/bash

filename=$1

# generate commit message
if [ ${filename: -4} == ".tex" ]; then
    message="creating .tex"
elif [ ${filename: -4} == ".pdf" ]; then
    message="creating .pdf"
else
    echo "error wrong input file"
    exit 1
fi

# commit and push if file changed
if git diff --exit-code -s $filename; then
    echo "Nothing to commit."
else
    git config --global user.name 'Luc Blassel'
    git config --global user.email 'luc.blassel@gmail.com'
    git add $filename
    git commit -m $message
    git push
fi

exit 0