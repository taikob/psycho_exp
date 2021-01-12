import os
import numpy as np
from natsort import natsorted
from stat_data import get as g

path= 'data'

def get_filename(path):

    data_list=list()


    for d in natsorted(os.listdir(path)):
        if not '_ans' in d and os.path.isfile(path+'/'+d) and '.txt' in d:
            d=d.replace('_'+d.split('_')[-1],'')
            if not d in data_list: data_list.append(d)

    return data_list

def combine_txt(file,path):
    number_list=list()
    for d in natsorted(os.listdir(path)):
        if not '_ans' in d and os.path.isfile(path+'/'+d) and '.txt' in d and file in d:
            number_list.append(d.replace(file,'').replace('.txt',''))

    with open(path + '/' + file + '.txt', 'w') as tx:
        with open(path+'/'+file + '_ans.txt','w') as an:
            for num in number_list:
                with open(path+'/'+file+num+'.txt'    ,'r') as f: txe = [s.strip() for s in f.readlines()]
                with open(path+'/'+file+num+'_ans.txt','r') as f: ane = [s.strip() for s in f.readlines()]
                for t in txe: tx.write(t+'\n')
                for a in ane: an.write(a+'\n')

data_list=get_filename(path)
for d in data_list:


    combine_txt(d,path)
    d=path+'/'+d+'.txt'
    with open(d,'r') as f: dt = f.readlines()
    with open(d.replace('.txt','_ans.txt'),'r') as a: da = a.readlines()

    aldata=list()
    for f in range(len(dt)):
        aldata.append(g.readtitleparam(dt[f])+[da[f].replace('\n','')])

    pp=2;vp=3;rs=4 #pp:original or mirror, vp: variable parameter(rotate speed), rs: answer
    sysparam, nump=g.get_sysparam(aldata, [0,1,2,3])

    print(sysparam)
    print(nump)

    datalist=list()
    for p in range(nump[pp]):
        datalist.append(np.zeros(nump[vp]))
    for ad in aldata:
        for p in range(nump[pp]):
            if float(ad[pp])==float(sysparam[pp][p]):
                ip=p
                break

        for v in range(nump[vp]):
            if float(ad[vp])==float(sysparam[vp][v]):
                datalist[ip][v]=datalist[ip][v]+float(ad[rs])

    for p in range(nump[pp]):
        datalist[p]/=(len(aldata) / nump[pp] / nump[vp])

    data=np.empty((nump[vp], nump[pp]+1))
    data[:,0]=sysparam[vp]
    for row in range(nump[pp]):
        data[:,row+1]=datalist[row]

    np.savetxt(d.replace('.txt','_data'+'.txt'), data)