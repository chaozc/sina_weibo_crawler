#coding=utf-8
import os
import urllib,urllib.request,urllib.parse
from http.cookiejar import LWPCookieJar 
#from HTMLParser import HTMLParser
import json
from sys import argv
import sys
import time
from login import ID_login
from parser import MyParser
from proxy_IPs import Proxy_IPs

class Crawler():

	def __init__(self, id_list_file='config/usr', cookieDir='cookies', num_id_th=0, usr_file='config/login_usr', keywords=[], data_dir='data', died_usr_file='config/died_usr', tmp_data_dir='tmp_data', date=''):
		self.id_list_file =id_list_file
		self.cookieDir = cookieDir
		self.num_id_th = num_id_th
		self.usr_file = usr_file
		self.login_usrs = []
		inf = open(self.usr_file, 'r')
		for line in inf:
			self.login_usrs.append(line[:-1])
		self.num_ids = len(self.login_usrs)
		self.keywords = keywords
		self.alive = self.num_ids
		self.tmp_data_dir =tmp_data_dir
		self.died_usr_file = died_usr_file
		self.data_dir = data_dir
		self.date = date

		self.ktot = {}
		for keyword in keywords:
			self.ktot[keyword] = 0
		self.tot = 0
		self.headers = [
			('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36'),
			('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
			('Accept-Charset','utf-8,ISO-8859-1;q=0.7,*;q=0.3'),
			('Accept-Encoding','none'),
			('Accept-Language','en-US,en;q=0.8'),
			('Connection','keep-alive'),
			('Host','s.weibo.com'),
		]
		self.ginfo = [
			{"loc":"北京", "id":"11:1000"},{"loc":"安徽", "id":"34:1000"},{"loc":"重庆", "id":"50:1000"},{"loc":"福建", "id":"35:1000"},{"loc":"甘肃", "id":"62:1000"},
			{"loc":"广东", "id":"44:1000"},{"loc":"广西", "id":"45:1000"},{"loc":"贵州", "id":"52:1000"},{"loc":"海南", "id":"46:1000"},{"loc":"河北", "id":"13:1000"},
			{"loc":"黑龙江", "id":"23:1000"},{"loc":"河南", "id":"41:1000"},{"loc":"湖北", "id":"42:1000"},{"loc":"湖南", "id":"43:1000"},{"loc":"内蒙古", "id":"15:1000"},
			{"loc":"江苏", "id":"32:1000"},{"loc":"江西", "id":"36:1000"},{"loc":"吉林", "id":"22:1000"},{"loc":"辽宁", "id":"21:1000"},{"loc":"宁夏", "id":"64:1000"},
			{"loc":"青海", "id":"63:1000"},{"loc":"山西", "id":"14:1000"},{"loc":"山东", "id":"37:1000"},{"loc":"上海", "id":"31:1000"},{"loc":"四川", "id":"51:1000"},
			{"loc":"天津", "id":"12:1000"},{"loc":"西藏", "id":"54:1000"},{"loc":"台湾", "id":"71:1000"},{"loc":"新疆", "id":"65:1000"},{"loc":"云南", "id":"53:1000"},
			{"loc":"浙江", "id":"33:1000"},{"loc":"陕西", "id":"61:1000"},{"loc":"香港", "id":"81:1000"},{"loc":"澳门", "id":"82:1000"},{"loc":"海外", "id":"400:1000"}]
		for i in range(35):
			#self.ginfo[i]['last'] = {}
			self.ginfo[i]['tot'] = {}
			for keyword in self.keywords:
				#self.ginfo[i]['last'][keyword] = {'time':'2015-04-06 21:00'}
				self.ginfo[i]['tot'][keyword] = 0
		"""
		self.reload(sys)   
		sys.setdefaultencoding('utf8') 
		"""
	def update(self):
		ouf = open(self.usr_file, 'w')
		for usr in self.login_usrs:
			if usr != None:
				ouf.write(usr+'\n')
		ouf.close()

	def crawl(self):
		ii = -1
		sttime = time.time()
		etime = 0
		page = 1
		loc = 0
		myparser = MyParser()
		#update = '2000-00-00 00:00'
		
		for keyword in self.keywords:
			for loc in range(35):
				for st in range(24):
					end = False
					for page in range(1, 50):
						if end:
							break
						while True:
							while True:
								ii += 1
								if ii == self.num_ids:
									ii = 0
								usr = self.login_usrs[ii]
								if usr != None:
									break

							print ('usr:', usr)
							cookieFile = self.cookieDir+'/'+usr
							cj = LWPCookieJar(cookieFile)
							cj.load(ignore_discard=True, ignore_expires=True)
							opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
							#opener.add_handler(urllib.request.ProxyHandler(proxies={"http":ip}))
							opener.addheaders = self.headers
							
							url = 'http://s.weibo.com/wb/'+urllib.parse.urlencode({'a':keyword})[2:]+'&xsort=time&timescope=custom:'+self.date+'-'+str(st)+':'+self.date+'-'+str(st)+'&region=custom:'+self.ginfo[loc]['id']+'&Refer=g&page='+str(page)
							

							print(url)
							print('Crawling:', keyword, self.ginfo[loc]['loc'], 'time:', str(st)+'-'+str(st+1), 'page:', page, 'lk_tot:', self.ginfo[loc]['tot'][keyword], 'k_tot:', self.ktot[keyword], 'tot:', self.tot)
							
							try:
								time1 = time.time()
								content = opener.open(url, timeout=15).read().decode('utf-8')
								time2 = time.time()
								dtime = time2-time1
							except:
								dtime = 100
							
							if dtime < 15:
								opener.close()
								print ('url opened...')
								if content.find('yzm_img') > 0:
									self.alive -= 1
									print ('usr:', usr, 'died, ', self.alive, 'users is still alive')
									oufd = open(self.died_usr_file, 'a')
									oufd.write(usr+'\n')
									oufd.close
									self.login_usrs[ii] = None
									self.update()
									if self.alive < self.num_id_th:
										exit()
								else:
									pos = content.find('"pid":"pl_wb_feedlist"')
									content = content[pos-1:]
									pos = content.find('</script>')
									content = content[:pos-1]

									try:
										js = json.loads(content)
									except:
										print('Json Load Error')
										continue
									
									html = ('<html>'+js["html"]+'</html>')
							
								
									if html.find('抱歉，未找到') > 0:
										end = True
										print('End of this interval')
										print('------------------------------------------------------------')
										break
									else:
										results = {}
										try:
											myparser.set_html(html)
											results = myparser.parse()
										except:
											print ('Parse Error')
										if len(results) > 0:
											ouf = open(self.data_dir+'/'+keyword+'/'+self.ginfo[loc]['loc'], 'a')
											for result in results:
												ouf.write(json.dumps(result, ensure_ascii = False))
												ouf.write('\n')
												self.ginfo[loc]['tot'][keyword] += 1
												self.ktot[keyword] += 1
												self.tot += 1

											ouf.close()
										
										print('Finish:', keyword, self.ginfo[loc]['loc'], 'page:', page, 'lk_tot:', self.ginfo[loc]['tot'][keyword], 'k_tot:', self.ktot[keyword], 'tot:', self.tot)							
										print('------------------------------------------------------------')
										#time.sleep(0.75)
										etime = 0
										break

							else:
								#self.alive -= 1
								etime += 1
								print ('Some Error Happend, Error times:', etime)
								print('------------------------------------------------------------')
								
								"""
								if etime == 300:
									exit()
								"""
		self.update()