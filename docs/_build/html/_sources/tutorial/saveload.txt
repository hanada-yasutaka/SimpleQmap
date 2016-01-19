
波動関数の保存及び読み込み
--------------------------

.. code:: python

    %matplotlib inline

波動関数の保存は savetxtで行う事ができる．

.. code:: python

    import SimpleQmap as sq
    import numpy as np
    import matplotlib.pyplot as plt
    
    dim = 60
    k = 1
    qmin, qmax = 0, 1
    pmin, pmax = -0.5,0.5
    
    cmap = sq.StandardMap(k=k)
    
    domain = [[qmin,qmax],[pmin,pmax]]
    qmap = sq.Qmap(cmap, dim, domain) # defines the quantum system
    evals, evecs = qmap.eigen() # return eigenvalues and list of eigenvector of the system. 
    
    fig, axs = plt.subplots(2,2,figsize=(8,8))
    
    print(axs)
    
    vec = evecs[0] # 0-th eigen vector
    
    q,p = vec.x[0],vec.x[1]
        
    axs[0][0].plot(q,vec.qrep().abs2(), '-')
    axs[0][1].plot(p,vec.prep().abs2(), '-')
    
    for ax in axs[0]:
        ax.semilogy()
    
    
    vec.savetxt("eigen_qrep_0.dat", rep="q")
    vec.savetxt("eigen_prep_0.dat", rep="p")
    #vec.savetxt("eigen_hsm_0.dat", rep="hsm")
    
    data0 = np.loadtxt("eigen_qrep_0.dat").T
    data1 = np.loadtxt("eigen_prep_0.dat").T
    
    axs[1][0].plot(data0[0],data0[1], '-')
    axs[1][1].plot(data1[0],data1[1], '-')
    
    for ax in axs[1]:
        ax.semilogy()
    
    plt.show()


.. parsed-literal::

    [[<matplotlib.axes._subplots.AxesSubplot object at 0x7fb91ec9e048>
      <matplotlib.axes._subplots.AxesSubplot object at 0x7fb91ec79208>]
     [<matplotlib.axes._subplots.AxesSubplot object at 0x7fb91ec82320>
      <matplotlib.axes._subplots.AxesSubplot object at 0x7fb91ec021d0>]]



.. image:: saveload_files/saveload_3_1.png


rep = "q" もしくは rep = "p"を指定して， savetxtを用いて波動関数
:math:`\ket{\phi}` を保存した場合，保存データは次のようになる．

:math:`x`\ を指定した座標として

1列目 :math:`x` 座標の値

2列目 :math:`x` 表示での波動関数の絶対値二乗
:math:`|\bracket{x}{\phi}|^2`

3列目 :math:`\bracket{x}{\phi}` の実部

4列目 :math:`\bracket{x}{\phi}` の虚部

である．

numpyのloadtxtを用いてこれらのデータを配列に格納することも可能であるが，表示の変換や伏見表示の計算をすぐに実行することができない為
SimpleQmap で定義されたloadtxtを使う事を勧める．
ただし，SimpleQmapは内部演算を行う際に表示を\ :math:`q`\ で統一しているため
:math:`p`
-表示波動関数をSimpleQmapのloadtxtで読み込んだ場合，自動的に:math:`q`
-表示に変換されるので注意して欲しい．

.. code:: python

    fig, axs = plt.subplots(1,2,figsize=(8,4))
    
    vec1 = sq.loadtxt("eigen_qrep_0.dat").T
    vec2 = sq.loadtxt("eigen_prep_0.dat").T
    
    axs[0].plot(q,vec1.abs2(), '-') 
    axs[1].plot(p,vec2.abs2(), '-') # wrong 


.. parsed-literal::

    load:eigen_qrep_0.dat
    dim:60
    domain:[0.000000,1.000000]x[-0.500000,0.500000]
    representation:q
    load:eigen_prep_0.dat
    dim:60
    domain:[0.000000,1.000000]x[-0.500000,0.500000]
    !!Warning!!
    convert original data (p-rep.) to q-rep.
    




.. parsed-literal::

    [<matplotlib.lines.Line2D at 0x7fb91e7bd550>]




.. image:: saveload_files/saveload_5_2.png


.. code:: python

    fig, axs = plt.subplots(1,2,figsize=(8,4))
    
    vec1 = sq.loadtxt("eigen_qrep_0.dat",verbose=False).T
    vec2 = sq.loadtxt("eigen_prep_0.dat",verbose=False).T
    
    axs[0].plot(q,vec1.qrep().abs2(), '-') 
    axs[1].plot(p,vec2.prep().abs2(), '-') # good




.. parsed-literal::

    [<matplotlib.lines.Line2D at 0x7fb91e35e8d0>]




.. image:: saveload_files/saveload_6_1.png


伏見表示は

.. code:: python

    fig, axs = plt.subplots(1,1,figsize=(6,6))
    
    x,y,z = vec1.hsmrep(col=100,row=100)
    axs.contour(x,y,z,100) 


.. parsed-literal::

    /home/hanada/anaconda3/lib/python3.4/site-packages/matplotlib/collections.py:650: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
      if self._edgecolors_original != str('face'):




.. parsed-literal::

    <matplotlib.contour.QuadContourSet at 0x7fb91eb3cc18>



.. parsed-literal::

    /home/hanada/anaconda3/lib/python3.4/site-packages/matplotlib/collections.py:590: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
      if self._edgecolors == str('face'):



.. image:: saveload_files/saveload_8_3.png


