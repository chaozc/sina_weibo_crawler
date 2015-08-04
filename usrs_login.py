from login import Usr_login
import time
class Usr_batch_login:
	def __init__(self, usr_list_file='config/usr', cookieDir='cookies', num_usrs=0, login_usr_file='config/login_usr'):
		self.usr_list = []
		inf = open(usr_list_file, 'r')
		for lines in inf:
			self.usr_list.append(lines[:-1].split('----'))
		self.usr_list_file =usr_list_file
		self.cookieDir = cookieDir
		self.num_usrs = num_usrs
		self.login_usr_file = login_usr_file


	def login(self):
		cnt = 0
		#login_info = []
		
		
		
		unused_usrs = []
		for item in self.usr_list:
			if cnt == self.num_usrs:
				unused_usrs.append(item)
				continue

			print (item[0], item[1])
			tmp = Usr_login(item[0], item[1], self.cookieDir)
			success, result = tmp.ssologin()
			if success:
				cnt += 1
				print (str(cnt)+'/'+str(self.num_usrs)+':', item[0], 'log in successfully')
				ouf = open(self.login_usr_file, 'a')
				ouf.write(item[0]+'\n')
				ouf.close()
			else:
				print ('[Error]: ', item[0], result)
				unused_usrs.append(item)
		
			print ('Sleep for a while to avoid frequently login')
			time.sleep(30)

		#Updating unused usr...
		ouf = open(self.usr_list_file, 'w')
		for item in unused_usrs:
			ouf.write(item[0]+'----'+item[1]+'\n')
		ouf.close()
		#return login_info
