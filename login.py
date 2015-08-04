import urllib,urllib.request,urllib.parse
from http.cookiejar import LWPCookieJar 
from bs4 import BeautifulSoup
import json
import time
import hashlib,hmac,base64,binascii,rsa
import json
#sometime this header is useful, because of Authorization field

#login to sina
class Usr_login:

	def __init__(self, user="", password="", cookieDir='.', proxy_IP=''):
		http_header = [
			('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36'),
			('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
			('Accept-Charset','utf-8,ISO-8859-1;q=0.7,*;q=0.3'),
			('Accept-Encoding','none'),
			('Accept-Language','en-US,en;q=0.8'),
			('Connection','keep-alive'),
			('Host','s.weibo.com'),
		]
		self.cookieFile = cookieDir+'/'+user
		ouf = open(self.cookieFile, 'w')
		ouf.write('#LWP-Cookies-2.0')
		ouf.close()
		self.cj = LWPCookieJar(self.cookieFile)
		self.cj.load(ignore_discard=True, ignore_expires=True)
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
		self.opener.add_handler(urllib.request.ProxyHandler(proxies={"http":proxy_IP}))
		self.opener.addheaders = http_header
		#get user information from params
		self.user,self.password = user,password

		#encode userid
		userid = bytes(urllib.parse.quote(self.user),'utf-8')
		self.encode_userid = base64.encodestring(userid)[:-1]


	#https to login
	#rsa2
	def ssologin(self):
		#get prelogin
		#fetch pubkey rsakv servertime nonce
		url = "https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)"
		time.sleep(0.5)
		print('Pubkey, rsakv, servertime and nonce obtained')
		res = self.opener.open(url).read().decode('utf-8')
		res = res[res.find("(")+1:-1]
		data = json.loads(res)
		nonce = data["nonce"]
		pubkey = data["pubkey"]
		rsakv = data["rsakv"]
		servertime = data["servertime"]

		
		#init rsa object
		rsaPublickey = int(pubkey, 16)
		key = rsa.PublicKey(rsaPublickey,65537)
		message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)
		message = bytes(message,"utf-8")
		sp = rsa.encrypt(message,key)
		sp = binascii.b2a_hex(sp)

		#to login
		baseurl = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
		params = {"entry":"sinaoauth","gateway":1,"from":"","savestate":0,\
				"useticket":1,"vsnf":0,"s":1,"su":self.encode_userid,\
				"service":"sinaoauth","servertime":servertime,"nonce":nonce,\
				"pwencode":"rsa2","rsakv":rsakv,"sp":sp,"encoding":"UTF-8",\
				"callback":"sinaSSOController.loginCallBack","cdult":2,"prelt":83,\
				"returntype":"TEXT"}
		rurl = baseurl + "?" + urllib.parse.urlencode(params)

		time.sleep(0.5)
		res = self.opener.open(rurl).read()
		res = res.decode('utf-8')
		print('Login responsed obtained')		

		self.cj.save(ignore_discard=True, ignore_expires=True)
		pos1 = res.find('(')
		pos2 = res.find(')')
		js = json.loads(res[pos1+1:pos2])
		retcode = js["retcode"]
		print(js)
		if retcode == '0':
			url = js["crossDomainUrlList"][0]
			time.sleep(0.5)
			try:
				self.opener.open(url, timeout=60)
			except:
				return False, 'Connection Timeout'
			self.cj.save(ignore_discard=True, ignore_expires=True)
			self.opener.close()
			return True, self.cookieFile
		else:
			reason = js["reason"]
			self.opener.close()
			return False, str(js)