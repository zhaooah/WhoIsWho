import os
import urllib2
import urllib
from sgmllib import SGMLParser

class GetProfile(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.name = ""
		self.pic=""
		self.right=1 #Check if picture is valid
		self.haspicture=0
	#When find correct div class,set flags
	def start_div(self,attrs):
		line = [v for k, v in attrs if k=='id']
		if line:
			if line[0] == 'profile-picture': 
				self.haspicture=1


	def start_img(self,attrs):
		line = [v for k, v in attrs if k=='class']
		if self.right==1:
			if line:
				if line[0] == 'photo': 
					for datatype, val in attrs:
						if datatype=='src':
							self.pic=val
						if datatype=='height' and val=='100':
							self.right=0
						if datatype=='alt':
							self.name=val



def generateAlbum(names):
	print 'Start generating html file...'
	page='<table style="width:480px"><tr>'
	for i in range(0,len(names)):
		if i!=0 and i%4==0:
			#Start a new line every 4 photos
			page=page+'</tr><tr>'
		page=page+'<td>'+'<img src="pic/'+ names[i]+'.jpg"><p>'+names[i]+'</p></td>'
	page=page+'</tr></table>'
	outfile = open('album.html',"w")
	outfile.write(page)
	outfile.close()


#Read linkedin list
file = open('NameList.txt', 'r')
NameList=file.read().splitlines()


#Create directory for storing pictures
if not os.path.exists('pic'):
    os.makedirs('pic')

print "Start fetching pictures..."

people=[]

for i in range(0,len(NameList)):
	#Get Page
	if NameList[i]!='':
		content = urllib.urlopen(NameList[i]).read()
		profile=GetProfile()
		profile.feed(content)
		if profile.haspicture==1:
			people.append(profile.name)
			print profile.name,profile.pic
			urllib.urlretrieve(profile.pic,'pic/'+profile.name+'.jpg')
		profile.close()

generateAlbum(people)


