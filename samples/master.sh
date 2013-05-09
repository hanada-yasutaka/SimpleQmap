#!/bin/bash
if [ $# != 1 ]; then
    echo "usage $0: eigen (or evolv) " 2<&1
    exit 1
fi
N=10
k=1.0 
qmin=0.0
qmax=1.0
pmin=0.0
pmax=1.0
TYPE=$1
export PYTHONPATH=../SimpleQmap:${PYTHONPATH}
if [ $TYPE == evolv ]; then
    python evolv.py $N $k $qmin $qmax $pmin $pmax
elif [ $TYPE == eigen ]; then
    python eigen.py $N $k $qmin $qmax $pmin $pmax
else
    echo "usage $0: eigen (or evolv)"
    exit 1
fi


list=('*_qrep_*.dat')

for name in ${list[@]}; do
    test -e ${name} || (echo "NOT exists ${name}" ; break)
    vqmin=$qmin
    vqmax=$qmax
    vpmin=$pmin
    vpmax=$pmax
    row=100
    col=100
    python ../SimpleQmap/qrep2hsm.py ${name} $vqmin $vqmax $vpmin $vpmax $row $col
    echo "${name} -> ${name/qrep/hsm}"
done

for hsm in *_hsm*.dat; do
    test -e ${hsm} || (echo "NOT exist ${name}" ; break)
    map=classical_map.dat
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

dir=StandardMap_${TYPE}_k${k}_N${N}
test -e ${dir} || (mkdir ${dir}; mkdir ${dir}/dat ${dir}/png)

mv *.dat ${dir}/dat/
mv *.png ${dir}/png/

echo '*.dat file moves to ${dir}/dat/ '
echo '*.png file moves to ${dir}/png/ '