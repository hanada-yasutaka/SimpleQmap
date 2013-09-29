PYTHON=(/opt/local/bin/python2.7 /opt/local/bin/python3.3)
for P in ${PYTHON[@]}; do
    for name in *.py; do
#	$P -m unittest -v ${name/.py/}
	$P ${name}
    done
done