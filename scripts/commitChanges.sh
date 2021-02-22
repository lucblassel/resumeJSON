#!/bin/bash

filename=$1

# generate commit message
if [ ${filename: -4} == ".tex" ]; then
    message="\"creating.tex\""
elif [ ${filename: -4} == ".pdf" ]; then
    message="\"creating.pdf\""
else
    echo "error wrong input file"
    exit 1
fi

echo "task is: $message"

# commit and push if file changed
if git diff --exit-code -s $filename; then
    echo "Nothing to commit."
else
    echo git config --global user.name 'Luc Blassel'
    git config --global user.name 'Luc Blassel'
    echo git config --global user.email 'luc.blassel@gmail.com'
    git config --global user.email 'luc.blassel@gmail.com'
    echo git add $filename
    git add $filename || exit 1
    echo git commit -m $message
    git commit -m $message || exit 1
    echo git push
    git push || exit 1
fi

exit 0
