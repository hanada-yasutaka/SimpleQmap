==========
Getting Start
==========

Requirements
--------

Mac OS X or Linux environment (does not support Windows)
SimpleQmap requires Python 2.5 or later. It has been tested with Python2.6, 2.7 and 3.3.

You'll need a following other package:
    
    1. numpy1.7.1 or later
    2. gcc (optional)
    3. gnuplot(optioal)
    

Download and Install
----------

　本チュートリアルはmac os もしくはlinux環境を想定しています．python2.7以上(python3系でも動くはず)を想定しています．
またパッケージはpypi等には登録していませんので，
`Web site <http://hanada-yasutaka.github.io/SimpleQmap/>`_
から最新版をDownloadし解凍して利用して下さい．


　ダウンロードしたフォルタ名がなんか嫌なので名前を変えるついでにホームディレクトリに移動させます．

.. code-block:: none

    $ mv ~/Downloads/hanada-yasutaka-SimpleQmap-72448f1 ~/SimpleQmap

別にSimpleQmap以外の名前でもかまわないです．

次にSimpleQmapをpythonからimportするためにPYTHONPATHを適切に通します．
適当なエディタで.bash_profileを開いて(例えば)

.. code-block:: none

    $ emacs ~/.bash_profile
    
で，次の一文をどこでもよいので付け加えてください．

.. code-block:: none

    export PYTHONPATH=~/SimpleQmap/:${PYTHONPATH}

emacs を終了し(controlキーを押した状態でx,cを続けて押す)設定を読み込むため，

.. code-block:: none

    $ source ~/.bash_profile

を実行して下さい．もしくはターミナルを再度開いて

.. code-block:: none

    $ python
    >>> import SimpleQmap

としてImportErrorが出なければSimpleQmapを利用することができます．

SimpleQmapのmoduleを最大限利用するため、ターミナルで

.. code-block:: none

    $ cd SimpleQmap/SimpleQmap/
    
に移動し，

.. code-block:: none
    
    $ bash make.sh
    
を実行してください．shared/libhsm.so という共有ファイルができていれば、
伏見表示を求めるルーチンを利用することができます．
もし，コンパイルできない場合は，gccをinstallすればできると思います．
伏見表示が必要なければコンパイルする必要はありません．




