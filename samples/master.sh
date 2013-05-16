#!/bin/bash
if [ $# != 1 ]; then
    echo "usage $0: eigen.py (or evolv.py) " 2<&1
    exit 1
fi
N=20
k=1.0 
qmin=0.0
qmax=1.0
pmin=0.0
pmax=1.0
PYFILE=$1
export PYTHONPATH=../SimpleQmap:${PYTHONPATH}

## python 
python ${PYFILE} $N $k $qmin $qmax $pmin $pmax 

if [ `echo $?` -ne 0 ]; then
    echo "usage $0: eigen.py (or evolv.py) "
    exit 0

fi
dir=StandardMap_${PYFILE/.py/}_k${k}_N${N}
test -e ${dir} || (mkdir ${dir}; mkdir ${dir}/dat )
echo "mkdir $dir"
echo "mkdir $dir/dat"

#### transfomation from q-rep to hsm-rep
list=(*_qrep_*.dat)
test -e ../SimpleQmap/shared/libhsm.so
if [ `echo $?` -eq 0 ]; then 
    test -e ${list}
    if [ `echo $?` -eq 0 ]; then
	for name in ${list[@]}; do
            vqmin=$qmin
            vqmax=$qmax
            vpmin=$pmin
            vpmax=$pmax
            row=100
            col=100
            python ../SimpleQmap/qrep2hsm.py ${name} $vqmin $vqmax $vpmin $vpmax $row $col
            echo "${name} -> ${name/qrep/hsm}"
	done
    fi
else
    echo "Worning: dose not compile libhsm.so"
fi

#### hsm data plot uging gnuplot
test -e `which gnuplot`
if [ `echo $?` -eq 0 ]; then 
    list=(*_hsm_*.dat)
    test -e ${list}
    if [ `echo $?` -eq 0 ]; then 
        for hsm in ${list[@]}; do   
            map=trajectories.dat
            echo "${hsm} -> ${hsm/.dat/.png}"
            gnuplot<<EOF
set term png size 600, 600 font arial 16
set output '${hsm/.dat/.png}'
set multiplot
set pm3d map
unset colorbox
set tit '${hsm}'
set xtics 0.5
set ytics 0.5
set xr [${qmin}:${qmax}]
set yr [${pmin}:${pmax}]
set palette defined( 0 "white", 0.2 "blue", 0.3 "#00ffff", 0.5 "#90ff90 ",0.6 "green", 0.7 "yellow", 0.8 "orange", 1.0 "red")
sp "${hsm}" tit ''
unset pm3d
set xl 'q'
set yl 'p'
sp "$map" u 1:2:(0.0) w d lc -1 tit ''
EOF
        done
    fi
else
    echo "Worning: gnuplot does not exist"
fi

test -e ${dir}/png || ( mkdir ${dir}/png )        
mv *.png ${dir}/png/
echo "mkdir $dir/png"    
echo '*.png file moves to ${dir}/png/ '    
mv *.dat ${dir}/dat/
echo '*.dat file moves to ${dir}/dat/ '
echo "Done."
