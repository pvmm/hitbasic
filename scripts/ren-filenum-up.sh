#!/bin/sh
# Rename test file by incrementing prefix number by one.

test_file_num=$1
echo "* selected number is $test_file_num"
DIR="$(cd "$(dirname "$0")" && pwd)"
cd ../tests/samples
mkdir tmp
num=$test_file_num

while :; do
    file_found=0
    printable=$(printf "%02d" $num)
    #echo "printable=$printable"

    for file in $printable*; do
        [ ! -f $file ] && break
        new_num=$(printf "%02d" $((num + 1)))
        new_file=$new_num$(expr substr $file 3 255)
        echo "Renaming $file to $new_file..."
        #mv "$file" "./tmp/$new_file"
        file_found=1
    done

    #echo "file_found=$file_found"
    if [ $file_found -ne 1 ]; then
        exit
    fi

    num=$((num + 1))
done

