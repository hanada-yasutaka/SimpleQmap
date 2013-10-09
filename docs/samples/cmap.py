import SimpleQmap as S
import numpy as np
import matplotlib.pyplot as plt

def evolv(q,p, Map):
    pp = p - Map.func0(q)
    qq = q + Map.func1(pp)
    return qq, pp

k=1.0
Map = S.StandardMap(k)
sample=100
iter = 500
q = np.random.random(sample)
p = np.random.random(sample)
for x in zip(q,p):
    q, p = x[0],x[1]
    traj = [np.array([]),np.array([])]
    for i in range(iter):
        q,p = evolv(q,p,Map)
        q = q - np.floor(q)
        p = p - np.floor(p)
        for j, x in enumerate([q,p]):
            traj[j] = np.append(traj[j], x)
    plt.plot(traj[0],traj[1], '.',markersize=3)
plt.xlabel('q',fontsize=22)
plt.ylabel('p',fontsize=22)
plt.savefig("std.png")
#plt.show()
