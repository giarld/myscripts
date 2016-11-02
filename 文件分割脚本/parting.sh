#!/bin/bash

if [ $# -ne 3 ];then
    echo "参数不正确"
    echo "参数：源文件名 单个文件大小 目标输出目录"
    exit
fi

filename=$1
subsize=$2
tpath=$3

filesize=`du -b $filename | awk '{print $1}'`

subbyte=`expr $subsize \* 1024`
subfileSum=`expr $filesize / $subbyte`

if [ `expr $filesize % $subsize` -ne 0 ];then
    subfileSum=`expr $subfileSum + 1`
fi

echo "将被分割为:$subfileSum个文件"
i=1
skipsum=0

while [ $i -le $subfileSum ]
do
    partname="$tpath/$filename"".part""$i"
    
    echo $partname

    dd if=$filename of=$partname bs=1024 count=$subsize skip=$skipsum
    i=`expr $i + 1`
    skipsum=`expr $skipsum + $subsize`

    sleep 1
done

md5sum $filename >> $tpath/md5sum.md5
echo '#!/usr/bin/python
# coding=utf-8
import os
tarName = "'$filename'"
if __name__ == "__main__":
    fileList = os.listdir("./")
    count = 0

    for fileName in fileList:
        if fileName.startswith(tarName + ".part"):
            count += 1

    for i in xrange(count):
        print "正在处理:", tarName, str(i + 1), "/", count
        if i == 0:
            os.system("cat " + tarName + ".part" + str(i + 1) + " > " + tarName)
        else:
            os.system("cat " + tarName + ".part" + str(i + 1) + " >> " + tarName)

    print "合并完成，正在检测完整性。"
    os.system("md5sum -c md5sum.md5")' > $tpath/merge.py

echo "分割完成"
