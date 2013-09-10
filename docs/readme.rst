Getting Start
==========

Website http://hanada-yasutaka.github.io/SimpleQmap/

Sorces https://github.com/hanada-yasutaka/SimpleQmap

Document http://simpleqmap.appspot.com/index.html

License
--------

SimpleQmap is distributed under the GNU LGPL license.


Requirements
--------

Mac OS X or Linux environment (does not support Windows)
SimpleQmap requires Python 2.5 or later. It has been tested with Python2.6, 2.7 and 3.3.

You'll need a following other package:
    
	1. numpy1.7.1 or later
	2. gcc (optional)
	3. gnuplot(optioal)

Download & installation
--------

You can download from github website

Documentation <http://simpleqmap.appspot.com/index.html>

To install, unpack the SimpleQmap archive and optionally run 

	cd SimpleQmap/
	bash make.sh

to work husimi-rep routine.

Example
--------
    
        cd samples/

        bash master.sh eigen.py # solve eigenvalue problem
        
    or 
        
	    bash master.sh evolv.py # solve initial value probrem
	    
書置
----------

本パッケージは量子カオス入門として作りましたが，ほとんどtestしていません．
制作者自信の研究目的に作っていません．
研究等で用いる際には沢山testして下さい．unittestが良いと思います．
そして，GitHubに全てのソースがあるのでDocumentやバグフィックスにご協力頂けると幸いです．
ただ，本パッケージはあくまで教育もくてきなので，大幅に機能増大はご勘弁下さい．

本パッケージ利用に伴い不利益を被る事になったとしても，制作者はいかなる責任をおいません．

花田康高(2013/05/17)




