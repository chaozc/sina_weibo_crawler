from bs4 import BeautifulSoup
import json
class MyParser:
	def __init__(self, html=''):
		self.html = html
	def set_html(self, html):
		self.html = html
	def get_result(self, div, arg0, arg1, arg2, arg3, f):
		result = {}
		div_ = div.find_all('div', arg0)[0]
		try:
			a = div_.find_all('a', arg1)[0]
		except:
			a = div_.find_all('a', 'name_txt W_fb')[0]
		result['usr'] = a['nick-name']
		p = div_.find_all('p', {'class':'comment_txt'})[0]
		result['wb'] = p.get_text()
		div__ = div_.find_all('div', {'class':'comment'})
		if len(div__) > 0:
			result['repost_from'] = self.get_result(div__[0], {'node-type':'feed_list_forwardContent'}, {'class':'W_texta W_fb'}, {'class':'feed_from W_textb'}, {'class':'feed_action_info'}, 0)
			div_ = div.find_all('div', arg2)[1]
		else:
			div_ = div.find_all('div', arg2)[0]
		aa = div_.find_all('a')
		try:
			result['time'] = aa[0]['title']
		except:
			result['time'] = aa[0].get_text()
		try:
			result['from'] = aa[1].get_text()
		except:
			result['from'] = ''

		ul = div.find_all('ul', arg3)[0]
		lis = ul.find_all('li')
		try:
			text = lis[0+f].get_text()
			result['no_repost'] = int(text[2:])
		except:
			result['no_repost'] = 0

		try:
			text = lis[1+f].get_text()
			result['no_reply'] = int(text[2:])
		except:
			result['no_reply'] = 0

		try:
			text = lis[2+f].get_text()
			result['no_like'] = int(text)
		except:
			result['no_like'] = 0
			
		return result
	def parse(self):
		soup = BeautifulSoup(self.html)
		#print (soup.prettify())
		lists = soup.find_all("div", {"class":'WB_cardwrap S_bg2 clearfix'})
		print (len(lists))
		results = []
		for div in lists:
			try:
				"""
				ouf = open('bb', 'a')
				ouf.write('---------------------------\n')
				ouf.write(str(div)+'\n')
				ouf.close()
				"""
				result = self.get_result(div, {'class':'feed_content wbcon'}, {'class':'W_texta W_fb'}, {'class':'feed_from W_textb'}, {'class':'feed_action_info feed_action_row4'}, 1)
			except:
				result = None
			
			if result != None:
				results.append(result)

		return results
"""
inf = open('tmp_data/股票_3416.html')
html = inf.read()
inf.close()

p = MyParser(html)
results = p.parse()
ouf = open('aa', 'w')
for result in results:
	ouf.write(json.dumps(result, ensure_ascii = False))
	ouf.write('\n')
ouf.close()

#print (html)

"""