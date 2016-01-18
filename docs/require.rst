================
はじめに
================

動作環境
-------------

Mac OS X か 一般的なLinux (windows機を持っていないので未検証)
Python 3系でないと動きません．テストはpython3.4で行っています．

(SimpleQmap v0.2よりpython2系では動かなくなりました)

You'll need a following other package:
    
    1. numpy1.7.1 or later
    2. gcc

チュートリアルを実行するためにはこの他に

    * matplotlib

をインストールして下さい．

pythonの事を何も知らないのであれば python の free distributionである 
`anaconda <https://www.continuum.io/downloads#_unix>`_
をインストールすることをおすすめします．

上記numpy及びmatplotlibはanacondaに同梱されています．
ユーザー(非管理者)権限で python環境を構築することができる為
OSの環境破壊を最小限に留める事が可能です．
その気になればUSBに環境を構築することもできます．

ちなみに公開されているpackageはpipを使ってinstallすることができます

.. code-block:: bash

    $ pip search mpmath # パッケージの検索
    $ pip install mpmath # パッケージのイントール

詳しくはgoogle等で検索して下さい．


ダウンロード & インストール
---------------------------------

SimpleQmapははpypi等に登録していないので，
`Web site (GitHub) <http://hanada-yasutaka.github.io/SimpleQmap/>`_
からDownloadして解凍して下さい(pipではインストールできませんし登録する気もありません)．



インストール方法はsetup.pyを利用してインストールする方法と，インストールせずに使用する方法を説明します．

* setup.py を使う場合

    ダウンロードしたパッケージを解凍しsetup.pyの置いてあるディレクトリに移動します．
    
    .. code-block:: bash
    
        $ cd SimpleQmap-0.2
        $ ls
        PKG-INFO  README  samples  setup.py  SimpleQmap
    
    
    このディレクトリで
    
    .. code-block:: bash
    
        $ python setup.py build
        $ python setup.py install
    
    を実行すればインストール終了です．
    build せずともinstall可能ですが，伏見表示の計算が実行できません．
    
    (i)pythonを起動し
    
    .. code-block:: python
    
        >>> import SimpleQmap
    
    でエラーが出なければインストールは成功です．ちなみにインストール先とバージョンの確認方法は次の通りです
    
    .. code-block:: python
    
        >>> SimpleQmap.__path__
        ['/home/hanada/anaconda3/lib/python3.4/site-packages/SimpleQmap']
        >>> SimpleQmap.__version__
        '0.2.1'
    
    アンインストールする場合は site-package/ まで潜って SimpleQmap のディレクトリとegg-info 
    (SimpleQmap-0.2-py3.4.egg-info みたいなファイル)を削除して下さい．
    
    .. todo::
    
        python setup.py instal した際に古いversionのeff-infoを自動的に消すように設定したい

* インストールせずに使う場合

    上記方法でインストールするのはソースパスが深い場所に潜ってしまうので，
    SimpleQmapのソースコードをじかに編集したい場合すこし面倒になります．
    インストールせずに使いたい場合は
    展開したzipファイル内にあるSimpleQmapをディレクトリを
    PYTHONPATHに設定して下さい．
    
    例えばホームディレクトにPyModulesを作ったとして，そこにSimpleQmapを置く場合を例示にあげると，
    展開したzipファイルの中にあるSimpleQmapを
    
    .. code-block:: bash
    
        $ unzip SimpleQmap-0.2.zip
        $ mv SimpleQmap ~/PyModules/ 
        
    PYTHONPATHの設定はbashの場合
    
    .. code-block:: python
    
        $ export PYTHONPATH=~/PyModules:${PYTHONPATH}
    
    とすれば設定できます．
    (~/.bash_profile or ~/.bashrc に上記命令を記述すればターミナルを開くたびに自動でPYTHONPATHが設定されます．$は記述しないでくだい)．
    
    更に伏見表示の計算を行う為に
    
    .. code-block:: bash
    
        $ cd ~/SimpleQmap
        $ bash make.sh
    
    を実行して下さい．ls を実行して shared/libhsm.so ファイルが作られていれば成功です．
    
    PyModules のディレクトとは **異なる** ディレクトにに移動して(i)pythonを起動し
    
    .. code-block:: python
    
        >>> import SimpleQmap
    
    を実行して何も出力されなければ設定完了です．もちろんpathは
    
        >>> SimpleQmap.__path__
        ['/home/hanada/PyModules/SimpleQmap']
    
    です．

    .. code-block:: python

        >>> import SimpleQmap
        ...
        ImportError: No module named 'SimpleQmap'
    
    となる場合はPYTHONPATHにホームディレクトリの短縮形(~/)を使わずにフルパスで設定してみて下さい．
    
    .. code-block:: python
        
        export PYTHONPATH=/home/youraccountname/PyModules:${PYTHONPATH} # for linux
        export PYTHONPATH=/Users/youraccountname/PyModules:${PYTHONPATH} # for mac
    
