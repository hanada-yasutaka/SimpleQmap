#!/bin/bash
file=libhsm
test -e ${file}.so && rm ${file}.so
include="/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/"
FLAGE="-Wall -fPIC"
CFILES="wrapper_HusimiRep.c HusimiRep.c CoherentState.c c_complex.c"
OFILES="wrapper_HusimiRep.o HusimiRep.o CoherentState.o c_complex.o"

gcc $FLAGE -c $CFILES -I${include} -I./
ar qc libhsm.a *o 
#gcc -shared -o ${file}.so ${OFILES}

