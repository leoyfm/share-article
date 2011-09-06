#!/usr/bin/env python
#coding=utf-8
import sys 
reload(sys) 
import feedparser
import urllib
import xmlrpclib
rssurl='http://www.google.com/reader/public/atom/user%2F16858515202600417432%2Fstate%2Fcom.google%2Fbroadcast'
usr='admin'
pwd='aXxS8onyCfCjXS'
url='http://www.mayifan.net/xmlrpc.php'
class WordPressPost:
	"""Represents post item
	"""	
	def __init__(self):
		self.postid = 0
		self.title = ''
		self.mt_keywords=''
		self.description = ''
		self.link = ''
		self.categories = []
		self.user = ''


server=xmlrpclib.ServerProxy(url)
m=server.system.listMethods()
print m
post = WordPressPost()	
post.title ='test' 
post.description='this is test' 
post.mt_keywords='software,'
post.categories.append('FunnyThing')  

server.metaWeblog.newPost('1', usr, pwd,post,True)


