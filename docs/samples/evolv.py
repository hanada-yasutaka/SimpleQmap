from SimpleQmap import Qmap, StandardMap
import matplotlib.pyplot as plt
import numpy as np

dim = 70
k = 1.0
qmin, qmax = 0.0, 1.0
pmin, pmax = -2.0, 2.0

tmax = 7
map = StandardMap(k=k)
domain = [[qmin,qmax],[pmin,pmax]]
qmap = Qmap(map, dim, domain)
#state = qmap.getState().cs(0.5,0.5)
state = qmap.getState()
state.insert(int(dim/2), 1.0+0.j)
init = state.p2q()

qmap.setInit(init)

for i in range(tmax):
    state = qmap.getIn()
    print("%d-th step" % i, state.norm())    
    pvec = state.prep()
    zero_index = (pvec.abs2() == 0.0)
    pvec[zero_index] = 1e-32 + 0.0j
    par = 1.*i/tmax
    plt.plot(state.scaleinfo.x[1],pvec.abs2(), '-',linewidth=3,color=plt.cm.jet(par), label='%d step' % i)
#    state.savetxt("evolv_qrep_%d.dat" % i)
    qmap.evolve()

plt.ylim(1e-28,1)
plt.ylabel(r"$|\psi_n(p)|^2$",fontsize=28)
plt.xlabel(r"$p$", fontsize=28)
plt.semilogy()
plt.legend()
plt.tight_layout()
plt.savefig("evolv_prep.png")
plt.show()