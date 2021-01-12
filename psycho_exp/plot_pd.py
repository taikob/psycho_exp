import os
import numpy as np
from natsort import natsorted
import matplotlib.pyplot as plt
import math
import scipy.optimize as so
from stat_data import get as g

path='data'

def model(x, mu,sig):
    #0: mu
    #1: sig
    err=np.empty(0)
    for xi in x:
        xxi=(mu-xi)/math.sqrt(2*sig)
        err=np.append(math.erf(xxi),err)

    return (1+err)/2

def residuals(coeffs, x, y):
    return y - model(x, coeffs)

for dir in natsorted(os.listdir(path)):
    if '_data.txt' in dir:
        print('try ', dir)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid(which="major", axis="x", color="blue", alpha=0.8,
                linestyle="--", linewidth=1)

        ax.grid(which="major", axis="y", color="green", alpha=0.8,
                linestyle="--", linewidth=1)

        data = np.loadtxt(path+'/'+dir)

        ydata = data[:, 1:data.shape[1]]
        plt.ylim(0, 1)
        plt.xlim(-5, 5)
        vrot = 0
        for yn in range(1, data.shape[1]):
            if yn==1:clr='red'
            else: clr='blue'

            param_bounds= ([min(data[:, 0]), 0], [max(data[:, 0]), max(data[:, 0])])
            coef, flag = so.curve_fit(model, data[:, 0], data[:, yn],  bounds=param_bounds)
            xvec=np.linspace(min(data[:, 0]), max(data[:, 0]), 100)
            fnp=model(xvec, coef[0], coef[1])

            ax.plot(data[:, 0], data[:, yn], '-o', linewidth=0.1,markersize=8, color=clr)
            ax.plot(xvec, fnp, '-', linewidth=1, color=clr)

            if yn==1: vrot =coef[0]
            else:     vrot-=coef[0]

        fig.savefig(path+'/'+dir.replace('.txt', '.png'), transparent=True)
        plt.close()

        vrot/=2
        np.savetxt(path+'/'+dir.replace('_data.txt','_vrot.txt'), np.array([vrot]))

g.file_param(path,'_vrot.txt')