
応用例
------

:doc: ``tutorial/std``

.. code:: python

    %matplotlib inline

.. code:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import SimpleQmap as sq
    
    twopi = 2.0*np.pi
    class HarperMap(sq.StandardMap):
        def __init__(self, k,a):
            sq.StandardMap.__init__(self,k)
            self.a = a
        def func1(self, x):
            return a*np.sin(twopi*x)/twopi
        def ifunc1(self,x):
            return -a*np.cos(twopi*x)/twopi/twopi
    
    def Map(q,p, cmap):
        pp = p - cmap.func0(q)
        qq = q + cmap.func1(pp)
        return [qq,pp]
    
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(1,1,1)
    
    sample=50
    tmax = 500
    k,a=1,1
    cmap = HarperMap(k,a)
    q = np.random.random(sample)
    p = np.random.random(sample)
    traj = [np.array([]),np.array([])]
    for i in range(tmax):
        q,p = Map(q,p,cmap)
        q = q - np.floor(q)
        p = p - np.floor(p)
        traj[0] = np.append(traj[0],q)
        traj[1] = np.append(traj[1],p)
    ax.plot(traj[0],traj[1],',k')
    plt.show()
