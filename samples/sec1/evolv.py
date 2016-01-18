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

tmax = 20
map = sq.StandardMap(k=k)

traj = Traj(map)

domain = [[qmin,qmax],[pmin,pmax]]
qmap = sq.Qmap(map, dim, domain) # defines the quantum system
state = qmap.getState().cs(0.0,0.0) # coherent state centered at (q,p) = (0,0)
qmap.setInit(state) # set intial condition

fig = plt.figure(figsize=(8,8))
plt.ion() # interactive mode of matplotlib
plt.show()

state = qmap.getIn()
for i in range(tmax):
    state.savetxt("data.dat",rep="p") # rep = "q", "p" or "hsm"
    
    ax0,ax1,ax2 = sq.utility.hsm_axes(fig)
    # drawing husimi-rep.
    x,y, z = state.hsmrep(50,50)
    ax0.contourf(x,y,z,50,cmap = sq.utility.hsm_cmap)
    ax0.plot(traj[0],traj[1],',k')
    ax0.set_xlim(qmin,qmax)
    ax0.set_ylim(qmin,qmax)
    
    # drawing q-rep
    ax1.plot(state.x[0], state.qrep().abs2(),'-k',lw=3)
    ax1.semilogy()
    ax1.set_xlim(qmin,qmax)
    ax1.set_ylim(1e-20,1)
    
    # drawing p-rep
    ax2.plot(state.prep().abs2(), state.x[1],'-k',lw=3)
    ax2.semilogx()
    ax2.set_ylim(qmin,qmax)
    ax2.set_xlim(1e-20,1)
    xtics =ax2.get_xticklabels()
    xtics[0].set_rotation(-90)
    
    
    fig.suptitle("%d-step" % i)
    
    fig.canvas.draw()
    _ = input("Press enter (or Ctrl-C to exit):")
    for ax in [ax0,ax1,ax2]:
        ax.clear()
    
    qmap.evolve() # calculate: | psi_1 > = U | psi_0 >
    state = qmap.getOut() # return: | psi_1 >
    #state = qmap.getIn() # return: | psi_0 >
