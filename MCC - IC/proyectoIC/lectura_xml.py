# coding: utf-8
from settings import *
from xml.dom import minidom
print "prueba_lectura_xml"
#doc = minidom.parse("general-tweets-train-tagged.xml")

for x in os.listdir(data):
	doc = minidom.parse(data+str(x))
	tweets = doc.getElementsByTagName("tweet")
	
	for tw in tweets:
		tweetid = tw.getElementsByTagName("tweetid")[0]
		user = tw.getElementsByTagName("user")[0]
		content = tw.getElementsByTagName("content")[0]
		if user.firstChild.data == 'LosadaPescador':
		    if content.firstChild:print("tweetid:%s, user:%s, content:%s" % (tweetid.firstChild.data, user.firstChild.data, content.firstChild.data))
		    else:print("tweetid:%s, user:%s, content:NONE" % (tweetid.firstChild.data, user.firstChild.data))
	