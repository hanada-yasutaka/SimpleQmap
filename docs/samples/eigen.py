from SimpleQmap import Qmap, StandardMap
import matplotlib.pyplot as plt
import numpy as np

dim = 70
k = 1.0
qmin, qmax = 0.0, 1.0
pmin, pmax = 0.0, 1.0
domain = [[qmin,qmax],[pmin,pmax]]

map = StandardMap(k=k)
qmap = Qmap(map, dim, domain)

evals, evecs = qmap.eigen() # get eigen value and eigen vectors

print("is unitary?",np.all(np.abs(np.abs(evals*np.conj(evals))-np.ones(dim))<1e-12))


fig = plt.figure(figsize=(6,6))
theta = np.linspace(-np.pi,np.pi, 500)
z = np.exp(-1.j*theta)
plt.plot(evals.real, evals.imag, 'o',markersize=8)
plt.plot(z.real, z.imag, '-k')
plt.xlim(-1.1,1.1)
plt.ylim(-1.1,1.1)
plt.grid()
plt.xlabel(r"$Re[u_n]$",fontsize=20)
plt.ylabel(r"$Im[u_n]$",fontsize=20)
plt.tight_layout()
plt.savefig("eigen_values.png")
plt.show()

#for i, evec in enumerate(evecs):
#    evec.savetxt("eigen_qrep_%i.dat" % i)

