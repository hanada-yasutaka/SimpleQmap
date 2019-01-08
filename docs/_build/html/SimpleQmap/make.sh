#!/bin/bash
# compile all makefile
cd source_files/
dirs=*/
make_list=(${dirs}make.sh)

#for make in ${make_list[@]}; do
for dir in ${dirs}; do
    echo "cd ${dir}"
    echo "---- complile shared library ----"
    echo "bash make.sh"
    cd $dir
    bash make.sh
    if [ `echo $?` -ne 0 ]; then
	echo "Stop: compile error in ${make}"
	exit 1
    fi
    echo "success ${dir}."
    echo ""
    cd ../
done
cd ..
