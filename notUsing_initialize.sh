#!/bin/bash
#File: initialize.sh
#Author: lxw
#Time: 2015-02-07
#Usage: Initialize(Create) the corresponding DIRECTORIES.

declare -a urlArr
i=0

for url in $(cat urls)
do
    urlArr[$i]="$url"
    i=$(($i+1))
done

for url in ${urlArr[@]}
do
    #lstrip
    url=${url/# /}

    #rstrip
    url=${url/% /}

    #replace "/" with "_", because no "/" allowed in a file/directory name.
    url=${url//\//_}

    #mkdir
    [ -d "${url}" ] || mkdir "${url}"
done
