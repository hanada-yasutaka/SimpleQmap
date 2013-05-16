# SimpleQmap

SimpleQmap is python calculator quantum chaotic map for an introduction.

Document <http://hanada-yasutaka.github.io/SimpleQmap/docs/_build/html/index.html>
#### License
SimpleQmap is distributed under the GNU LGPL license.

#### Requirements
* Mac OS X or Linux environment (does not support Windows)
* SimpleQmap requires Python 2.5 or later. It has been tested with Python2.6, 2.7 and 3.3.
* You'll need a following other package:

	1. numpy1.7.1 or later
	2. gcc (optional)
	3. gnuplot(optioal)

#### Download & installation

You can download from github website
<https://github.com/hanada-yasutaka/SimpleQmap> (click zip button)

To install, unpack the SimpleQmap archive and optionally run 

	cd SimpleQmap/
	bash make.sh

to work husimi-rep routine.

#### Example

	cd samples/
	bash master.sh eigen.py # solve eigenvalue problem

or 

	bash master.sh evolv.py # solve initial value probrem

#### Known probrems
SimpleQmap does not work python3.3

	f = open("test.dat","w")
	numpy.savetxt(f, numpy.array([1,2,3]))
	   1045         else:
	   1046             for row in X:
	-> 1047                 fh.write(asbytes(format % tuple(row) + newline))
	   1048         if len(footer) > 0:
	   1049             footer = footer.replace('\n', '\n' + comments)

	TypeError: must be str, not bytes
