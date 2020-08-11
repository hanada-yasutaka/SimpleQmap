import SimpleQmap as sq
import numpy as np
import matplotlib.pyplot as plt

twopi = 2.0*np.pi


dim = 30
k = 1
qmin, qmax = -np.pi, np.pi
pmin, pmax = -np.pi, np.pi

domain = np.array([[qmin,qmax],[pmin,pmax]])
scaleinfo = sq.ScaleInfo(dim, domain)
#qmap = sq.Qmap(map, dim, domain) # defines the quantum system
#evals, evecs = qmap.eigen() # return eigenvalues and list of eigenvector of the system.

Solver = sq.qmap.TVHamiltonian(dim, domain)
T = lambda x: x**2/2
V = lambda x: np.cos(x)

matT = Solver.matTqrep(T)
matV = Solver.matVqrep(V)
hbar = Solver.hbar
s = (-1.j/hbar)
matHam1 = matT +  matV
matHam2 = (matT * matV - matV * matT)/2
matHam = matHam1 + s * matHam2 

from SimpleQmap.utility import hsm_axes
fig = plt.figure()
ax1, ax2, ax3 = hsm_axes(fig)
ax = [ax1, ax2, ax3]

evals, evecs = matHam.eigh()
#init_vec = sq.State(scaleinfo)
#coef = np.array([vec.inner(init), ]a

plt.ion()
plt.show()

x = np.linspace(domain[0,0], domain[0,1], 100)
y = np.linspace(domain[1,0], domain[1,1], 100)
Q,P = np.meshgrid(x,y)


for i in range(dim):

    vec = evecs[i]  
    
    x,y,z = vec.hsmrep()
    ax[0].contourf(x,y,z, cmap=plt.cm.Oranges)
    ax[0].contour(Q, P, T(P)+V(Q), 10)

    q = vec.x[0]    
    ax[1].plot(q, vec.abs2(), "-")
    ax[1].semilogy()
    ax[1].set_ylim(1e-30, 1)

    p = vec.x[1]
    prep = vec.prep().abs2()
    ax[2].plot(prep, q,"-")
    ax[2].semilogx()    
    ax[2].set_xlim(1e-30, 1)    


    fig.suptitle("%d-th eigenstate, E_n=%f" % (i, evals[i]))
    fig.canvas.draw()
    _ = input()
    for a in ax:
        a.cla()
