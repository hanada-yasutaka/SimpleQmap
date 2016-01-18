import SimpleQmap as sq
import numpy as np
import matplotlib.pyplot as plt

def Traj(map,sample=100,tmax=500):
    q = np.random.random(sample)
    p = (np.random.random(sample) -0.5) * (pmax - pmin) * 2
    res = [np.array([])]*2
    for i in range(tmax):
        pp = p - map.func0(q)
        qq = q + map.func1(pp)
        q = qq - np.floor(qq)
        p = pp - np.floor(pp)
        res[0] = np.append(res[0],q)
        res[1] = np.append(res[1],p)
    return res


dim = 70
k = 1
qmin, qmax = 0, 1
pmin, pmax = 0, 1 

map = sq.StandardMap(k=k)

traj = Traj(map)

domain = [[qmin,qmax],[pmin,pmax]]
qmap = sq.Qmap(map, dim, domain) # defines the quantum system
evals, evecs = qmap.eigen() # return eigenvalues and list of eigenvector of the system. 

fig = plt.figure(figsize=(8,8))
plt.ion()
plt.show()

for i, evec in enumerate(evecs):
    #evec.savetxt("data.dat",rep="p") # rep = "q", "p" or "hsm"
    
    ax0,ax1,ax2,ax3 = sq.utility.hsm_axes1(fig)
    # drawing husimi-rep.
    x,y, z = evec.hsmrep(50,50)
    ax0.contourf(x,y,z,50,cmap = sq.utility.hsm_cmap)
    ax0.plot(traj[0],traj[1],',k')
    ax0.set_xlim(qmin,qmax)
    ax0.set_ylim(qmin,qmax)
    
    # drawing q-rep
    ax1.plot(evec.x[0], evec.qrep().abs2(),'-k',lw=3)
    ax1.semilogy()
    ax1.set_xlim(qmin,qmax)
    ax1.set_ylim(1e-20,1)
    
    # drawing p-rep
    ax2.plot(evec.prep().abs2(), evec.x[1],'-k',lw=3)
    ax2.semilogx()
    ax2.set_ylim(qmin,qmax)
    ax2.set_xlim(1e-20,1)
    xtics =ax2.get_xticklabels()
    xtics[0].set_rotation(-90)
    
    # drawing eigenvalues
    theta = np.linspace(-np.pi,np.pi,100)
    z = np.exp(-1.j*theta)
    ax3.plot(z.real,z.imag, '-g')
    ax3.plot(evals.real, evals.imag, 'ob')
    ax3.plot(evals[i].real, evals[i].imag, 'or',markersize=10)
    ax3.set_title("eigen_values")
    
    
    fig.suptitle("%d-th eigenstate" % i)
    
    fig.canvas.draw()
    _ = raw_input("Press enter (or Ctrl-C to exit):")
    for ax in [ax0,ax1,ax2,ax3]:
        ax.clear()
