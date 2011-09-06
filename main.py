#!/usr/bin/env python
#coding=utf-8
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
import feedparser
import urllib
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext import webapp
import wsgiref.handlers
from google.appengine.ext.webapp.util import run_wsgi_app
import xmlrpclib
import re, string, time, operator
from types import *

rssurl='http://www.google.com/reader/public/atom/user%2F16858515202600417432%2Fstate%2Fcom.google%2Fbroadcast'
usr='LEO'
pwd='mayifan'
url='http://www.mayifan.net/xmlrpc.php'
#create db
class Article(db.Model):
	title = db.StringProperty()
	author = db.StringProperty()
	content = db.TextProperty()
	#tag = db.ListProperty()
	tag = db.StringProperty()
	isread = db.BooleanProperty()
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

class MainPage(webapp.RequestHandler):
	def get(self):
		self.rssurl='http://www.google.com/reader/public/atom/user%2F16858515202600417432%2Fstate%2Fcom.google%2Fbroadcast'
		self.usr='LEO'
		self.pwd='mayifan'
		self.url='http://www.mayifan.net/xmlrpc.php'
				
		self.server=xmlrpclib.ServerProxy(self.url)
		self.feed = feedparser.parse(self.rssurl)

		self.response.out.write('<html><body>')
		
		self.response.out.write('<p>check</p></ br>')
		self.checkrss()
		self.response.out.write('<p>update</p></ br>')
		self.sendtoBlog()
		self.response.out.write('</body></html>')
	
	def checkrss(self):
		for entry in self.feed.entries:
			self.response.out.write('<p>find %s</p></ br>' %entry.title)
			contents = ""
			tags=''
			try:
				for t in entry['tags']:
					tags +=t['term'] + ','
			except KeyError:
				print '<p>tag is none</p></ br>'
				tags=''
			try:
				contents = entry.content[0]['value']
			except AttributeError:
				contents = entry.summary
			articles = db.GqlQuery("SELECT * FROM Article WHERE title = :1", entry.title)
			q = articles.get()
			#if articles.get() is None:
			if q is None:
				self.response.out.write('<p>update one to db</p> </ br>')
				Article( title=entry.title,author= entry.author,tag=tags, content=contents, isread=False ).put()
			else:
				self.response.out.write('<p> select title is %s</p></ br>' %q.title)
	def sendtoBlog(self):
		articles = db.GqlQuery('SELECT * FROM Article WHERE isread = False')
		#articles = Article.all()
		#articles.filter('isread=', False)
		q = articles.get()
		if q is not None:
			self.response.out.write('<p>prepare to send to wordpress</p> </ br>')
			post = WordPressPost()	
			post.title = q.title
			content=''
			content +=q.content
			post.description= content
			post.mt_keywords=q.tag
			post.categories.append('FunnyThing')  

			self.response.out.write('<p>send article title: %s</p> </ br>' %post.title)
			try:
				self.server.metaWeblog.newPost('1', self.usr, self.pwd,post,True)
			except:
				pass
			q.isread = True
			q.put()
			self.response.out.write('<p>send wordpress sucess</p></ br>')
		else:
			self.response.out.write('<p> no article need to send</p></ br>' )
'''
class rssshare:
	def __init__(self,url,rssurl,usr,pwd):
		self.url=url
		self.rss=rssurl
		self.user=usr
		self.password=pwd
		self.server=xmlrpclib.ServerProxy(self.url)
		self.feed = feedparser.parse(self.rss)
	def checkrss(self):
		for entry in self.feed.entries:
			contents = ""
			tags=''
			try:
				for t in entry['tags']:
					tags +=t['term'] + ','
			except KeyError:
				print '<p>tag is none</p></ br>'
				tags=''
			try:
				contents = entry.content[0]['value']
			except AttributeError:
				contents = entry.summary
			articles = db.GqlQuery("SELECT * FROM Article WHERE title = :1", entry.title)
			if articles.get() is None:
				print '<p>update one</p></ br>'
				Article( title=entry.title,author= entry.author,tag=tags, content=contents, isread=False ).put()
	def update(self):
		articles = db.GqlQuery('SELECT * FROM Article WHERE isread = False')
		#articles = Article.all()
		#articles.filter('isread=', False)
		q = articles.get()
		if q is not None:
			post = WordPressPost()	
			post.title = q.title
			content=''
			content +=q.content
			post.description= content
			post.mt_keywords=q.tag
			post.categories.append('FunnyThing')  

			print post.title 
			print q.title
			print post.description
			print q.content
			print post.mt_keywords
			print q.tag
			print post.categories  
			pid =self.server.metaWeblog.newPost('1', self.user, self.password,post,True)
			if pid >1:
				q.isread = True
				q.put()
				print '<p>sucess</p></ br>'
'''

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
