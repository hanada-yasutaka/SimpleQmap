from SimpleQmap import Qmap, StandardMap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

nullfmt = NullFormatter() 

def frame(figsize=(8,8)):
	left, width = 0.1, 0.5
	bottom, height = 0.1, 0.5
	bottom_h = left_h = left+width+0.02

	r1 = [left, bottom, width, height]
	r2 = [left, bottom_h, width, 0.3]
	r3 = [left_h+0.01, bottom, 0.3, height]

	fig = plt.figure(1,figsize=figsize)
	ax1 = plt.axes(r1)
	ax2 = plt.axes(r2)
	ax3 = plt.axes(r3)
	ax2.xaxis.set_major_formatter(nullfmt)
	ax3.yaxis.set_major_formatter(nullfmt)
	ax = [ax1,ax2,ax3]
	return ax
	
def cmap(q,p,Map):
	pp = p - Map.func0(q)
	qq = q + Map.func1(pp)
	return qq, pp
	
def trajectory(Map, sample=100,iter=500):
	q = np.random.random(sample)
	p = np.random.random(sample)
	traj = [np.zeros([]),np.zeros([])]
	for i in range(iter):
		q,p = cmap(q,p,Map)
		q = q - np.floor(q)
		p = p - np.floor(p)
		for j,x in enumerate([q,p]):
			traj[j] = np.append(traj[j],x)
	return traj
	
dim = 70
k = 1.0
qmin, qmax = 0.0, 1.0
pmin, pmax = 0.0, 1.0
domain = [[qmin,qmax],[pmin,pmax]]

map = StandardMap(k=k)
qmap = Qmap(map, dim, domain)

evals, evecs = qmap.eigen() # get eigen value and eigen vectors
traj = trajectory(map)
for i, evec in enumerate(evecs):
	print(i)
	ax = frame()
	X,Y,Z = evec.hsmrep(100,100)
	ax[0].contour(X,Y,Z,100,cmap=plt.cm.jet)
	ax[0].plot(traj[0],traj[1],',',color='#bebebe')		
	ax[0].set_xlabel("q",fontsize=20)
	ax[0].set_ylabel("p",fontsize=20)
	
	ax[1].plot(evec.scaleinfo.x[0],evec.qrep().abs2())
	ax[1].set_title("%d-th eigen state" % i)	
	ax[1].set_ylabel(r"$|\Psi_n(q)|^2$",fontsize=15)

	ax[2].plot(evec.prep().abs2(),evec.scaleinfo.x[1])
	ax[2].set_xlabel(r"$|\Psi_n(p)|^2$",fontsize=15)	
	ax[2].set_xticklabels(ax[2].get_xticks(),rotation=45)
	plt.savefig("eigen_state_%d.png" % i)
	plt.close()
	
	if i == 3:
		break
#	plt.show()