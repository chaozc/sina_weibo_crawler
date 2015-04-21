import urllib.parse
from ids_login import ID_batch_login
from main_crawler import Crawler
import imp
import sys
import time
"""
t = ID_batch_login(num_ids=20)
t.login()


for i in range(20, 1, -1):
	print (i, 'minutes left')
	time.sleep(60)
time.sleep(60)
"""
inf = open('task.txt', 'r')
keywords = []
for line in inf:
	if not (line[:-1] in keywords):
		keywords.append(line[:-1])
inf.close()
t = Crawler(num_id_th=46, keywords=keywords, date='2015-04-08', data_dir='data-04-08')
t.crawl()

#print ()

#print ()


