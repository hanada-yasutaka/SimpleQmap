#!/bin/bash
# compile wrapper_hsmrap
fname=libhsm
dir=../../shared
test -e ${fname}.so  && rm ${fname}.so 
list=(*.o)
test -e ${list} && rm *.o

#include="/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/"

FLAGE="-Wall -fPIC"
CFILES="wrapper_HusimiRep.c CoherentState.c HusimiRep.c c_complex.c"
OFILES="wrapper_HusimiRep.o CoherentState.o HusimiRep.o c_complex.o"
echo "gcc $FLAGE -c $CFILES -I/usr/include/python2.7 -lm"
gcc $FLAGE -c $CFILES -I/usr/include/python2.7 -I./
gcc -shared -o libhsm.so ${OFILES}
echo "gcc -shared -o libhsm.so ${OFILES} -lm"


if [ `echo $?` -ne 0 ]; then
    echo "Error: compile error"
    eixt 1
fi
test -e ${dir} || mkdir ${dir}
mv ${fname}.so ${dir}/
echo "Success: make ${fname}.so in ${dir/..\//}/ directroy."
