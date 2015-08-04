import urllib.parse
from usrs_login import Usr_batch_login
from main_crawler import Crawler
import imp
import sys
import time
from sys import argv
import os
"""
t = Usr_batch_login(num_usrs=39)
t.login()



"""
def compare(d1, d2):
	for i in range(3):
		if d1[i] > d2[i]:
			return 1
		elif d1[i] < d2[i]:
			return -1
	return 0
def next(d):
	nd = [0, 0, 0]
	nd[2] = d[2]+1
	if (nd[2] == 32 and d[1] in [1, 3, 5, 7, 8, 10, 12]) or (nd[2] == 31 and d[1] in [4, 6, 9, 11]) or (nd[2] == 30 and d[1] == 2) or (nd[2] == 29 and d[1] == 2 and (d[0]%400 == 0 or (d[0]%4 == 0 and d[0]%100 >0))):
		nd[2] = 1
		nd[1] = d[1]+1
		if nd[1] == 13:
			nd[1] = 1
			nd[0] = d[0]+1
		else:
			nd[0] = d[0]
	else:
		nd[1], nd[0] = d[1], d[0]
	return nd
if __name__ == "__main__":
	taskf, start_date, end_date, data_dir, gap = argv[1], argv[2], argv[3], argv[4], argv[5]
	if len(argv) == 7:
		status = {'keyword':argv[6]}
	else:
		status = {}
	inf = open(taskf, 'r')
	keywords = []
	for line in inf:
		if not (line[:-1] in keywords):
			keywords.append(line[:-1])
	inf.close()
	sd = start_date.split('-')
	sd = [int(item) for item in sd]
	ed = end_date.split('-')
	ed = [int(item) for item in ed]
	try:
		os.mkdir(data_dir)
	except:
		pass
	#time.sleep(3600)
	"""
	l = Usr_batch_login(num_usrs=40)
	l.login()
	exit()
	"""
	while compare(sd, ed) <= 0:
		ssd = [str(item) if len(str(item)) > 1 else '0'+str(item) for item in sd]
		date = '-'.join(ssd)
		try:
			os.mkdir(data_dir+'/'+date)
		except:
			pass
		for keyword in keywords:
			try:
				os.mkdir(data_dir+'/'+date+'/'+keyword)
			except:
				pass
		while True:
			t = Crawler(num_usr_th=36, keywords=keywords, date=date, data_dir=data_dir+'/'+date, status=status, gap=gap)
			status = t.crawl()
			if status == {}:
				break
			else:
				l = Usr_batch_login(num_usrs=40)
				l.login()
		sd = next(sd)
#print ()

#print ()


