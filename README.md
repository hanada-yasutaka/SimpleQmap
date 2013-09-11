# SimpleQmap

SimpleQmap is python calculator quantum chaotic map for an introduction.

Website <http://hanada-yasutaka.github.io/SimpleQmap/>

Document <http://simpleqmap.appspot.com/index.html>
#### License
SimpleQmap is distributed under the MIT license.

#### Requirements
* Mac OS X or Linux environment (does not support Windows)
* SimpleQmap requires Python 2.5 or later. It has been tested with Python2.6, 2.7 and 3.3.
* You'll need a following other package:

	1. numpy1.7.1 or later
	2. gcc (optional)
	3. gnuplot(optioal)

#### Download & installation

You can download from github website

To install, unpack the SimpleQmap archive and optionally run 

	cd SimpleQmap/
	bash make.sh

to work husimi-rep routine.

#### Example

	cd samples/
	bash master.sh eigen.py # solve eigenvalue problem

or 

	bash master.sh evolv.py # solve initial value probrem
