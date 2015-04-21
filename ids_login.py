from proxy_IPs import Proxy_IPs
from login import ID_login
class ID_batch_login:
	def __init__(self, id_list_file='config/usr', cookieDir='cookies', num_ids=0, usr_IP_file='config/login_usr'):
		self.id_list = []
		inf = open(id_list_file, 'r')
		for lines in inf:
			self.id_list.append(lines[:-1].split('----'))
		self.id_list_file =id_list_file
		self.cookieDir = cookieDir
		self.num_ids = num_ids
		self.usr_IP_file = usr_IP_file
		"""
		if self.num_IP > 0:
			tmp = Proxy_ids()
			tmp.set_param(tqsl=str(num_IP))
			self.IP_list = tmp.get_id_list()
		else:
			self.num_IP = 1
			self.IP_list = ['']
		"""

	def login(self):
		cnt = 0
		#login_info = []
		
		
		
		unused_ids = []
		for item in self.id_list:
			if cnt == self.num_ids:
				unused_ids.append(item)
				continue
			"""
			tmp = Proxy_IPs(1)
			self.IP_list = tmp.get_ip_list()
			ip = self.IP_list[0] 
			"""
			print (item[0], item[1])
			tmp = ID_login(item[0], item[1], self.cookieDir)
			success, result = tmp.ssologin()
			if success:
				#login_info.append([item[0], result, ip])
				cnt += 1
				print (str(cnt)+'/'+str(self.num_ids)+':', item[0], 'log in successfully')
				ouf = open(self.usr_IP_file, 'a')
				ouf.write(item[0]+'\n')
				ouf.close()
				#ouf.write(item[0]+'----'+item[1]+' '+ip+'\n')
			else:
				print ('[Error]: ', item[0], result)
				unused_ids.append(item)
		

		#Updating unused usr...
		ouf = open(self.id_list_file, 'w')
		for item in unused_ids:
			ouf.write(item[0]+'----'+item[1]+'\n')
		ouf.close()
		#return login_info