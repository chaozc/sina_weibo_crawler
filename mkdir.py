#coding=utf-8
import os
def mkdir(lfile, dirr):
	inf = open(lfile, 'r')
	dlist = inf.readlines()
	inf.close()
	for d in dlist:
		d = d[:-1]
		if not os.path.isdir(dirr+'/'+d):
			os.mkdir(dirr+'/'+d)

mkdir('task.txt', 'data-04-09')