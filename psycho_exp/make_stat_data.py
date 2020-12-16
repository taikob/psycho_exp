import os
import numpy as np
from stat_data import get as g
from natsort import natsorted
path='.'

cn=2
#color num :
# 1 -> one color
# 2 -> two color

out=np.empty((0, cn+1))
for dir in natsorted(os.listdir(path)):
    if '_vrot.txt' in dir:
        data = np.loadtxt(path+'/'+dir)
        data = float(data)
        tprm=g.readtitleparam(dir)
        if cn==1:
            out=np.append(out,np.array([[int(tprm[0]),data]]), axis=0)
        elif cn==2:
            print([int(tprm[0]),int(tprm[1]),data])
            out=np.append(out,np.array([[int(tprm[0]),int(tprm[1]),data]]), axis=0)

np.savetxt(path+'/'+'vrot_stat_data.csv', out, delimiter=',')