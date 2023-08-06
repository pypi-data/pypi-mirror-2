#!/bin/bash
#
# This script instruments ecdsa.py

py_lst=(pypy \
        python2.4 \
        python2.5 \
        python2.6 \
        python2.7 \
        python3.1 \
        python3.2)
py_lst_len=${#py_lst[*]}

i=0
while [ $i -lt $py_lst_len ]; do
    bin=`command -v ${py_lst[$i]}`
    let i++

    if [ -z $bin ]; then
	continue
    fi

    cmd="$bin ecdsa.py"
    echo ">> $cmd"
    $cmd
    echo
done

exit 0
