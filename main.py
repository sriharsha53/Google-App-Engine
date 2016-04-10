#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from google.appengine.ext import db
from google.appengine.api import users
import webapp2
import cgi
import urllib
import math

class Database(db.Model):
	author=db.UserProperty()
	name=db.StringProperty(multiline=True)
	number=db.IntegerProperty(required=False)
	prop=db.StringProperty(required=False,choices=set(["pallindrome","not pallindrome"]))
	prop2=db.StringProperty(required=False,choices=set(["prime","not prime"]))
	date= db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	self.response.write('<html><head><link rel="Stylesheet" type="text/css" media="screen" href="/stylesheets/style.css">')
    	self.response.write('<title>Number Statistics</title></head>')
    	self.response.write('<body><h1 class="main"><center>Number statistics</center></h1>')
    	user=users.get_current_user()
    	if user:
    		self.response.write('<h3 class="headi">Hello %s![<a href=%s>sign out</a>]</h3>' %\
    		 (user.nickname(),users.create_logout_url(self.request.uri))
    		 )
    	else:
    		self.redirect(users.create_login_url(self.request.uri))
    		return
    		        
        self.response.write("""<form action="/palli" method="post">
        	<input type="number" name="num">
        	<input type="submit" name="check" class="button1" value="check">
        	<input type="submit" name="clear" class="button4" value="clear">
        	</form><hr>
        	
        	""")

        self.response.write('<h3>History</h3><ol>')
        databases = Database.all().order('-date').fetch(10)
        for database in databases:
        	self.response.write('<li>user name: %s' % database.name)
        	self.response.write('<br>number entered:%s' % database.number)
        	self.response.write('<br>%s' % database.prop)
        	self.response.write('<br>%s' % database.prop2)
        self.response.write('</ol>')	
        # self.response.write('<html><body>')
       

class PallindromeChecker(webapp2.RequestHandler):
	def post(self):
		self.response.write('<link rel="Stylesheet" type="text/css" media="screen" href="/stylesheets/style.css">')
		if(self.request.get('clear')):
			q = db.GqlQuery("SELECT * FROM Database")
			results = q.fetch(5)
			while results:
			    db.delete(results)
			    results = q.fetch(5, len(results))
			self.redirect('/') 
			

		else:
			out1=0
			n=int(self.request.get('num'))
			self.response.write('<h4 class="ans">The number is : %s</h4>' % n)
			self.response.write('<br>')
			r=0
			num=n
			new=0
			while(n>0):
				r=n%10
				new=r+(new*10)
				n=n/10
			if(new==num):
				out1=1
				self.response.write("<h5>It's a pallindrome</h5>")
			else:
				out1=2
				self.response.write("<h5>It's not a pallindrome</h5>")	

			out2=0
			n=int(self.request.get('num'))
			if n==1 or n==0:	
				self.response.write("<h5>It's not a prime number</h5>")
			else:
				i=2
				c=0
				self.response.write('<br>')
				while(i<=math.sqrt(n)):
					if(n%i==0):
						c=c+1
					i=i+1		
				if(c>0):
					out2=1
					self.response.write("<h5>It's not a prime number</h5>")
						
				else:
					out2=2
					self.response.write("<h5>It's a prime number</h5>")
			database=Database()
			user=users.get_current_user()
			if user:
				database.author = user
			database.name = user.nickname()
			database.number=n
			if(out1==1):
				database.prop='pallindrome'
			else:
				database.prop='not pallindrome'	
			if(out2==1):
				database.prop2='not prime'
			else:
				database.prop2='prime'		
			database.put()
			self.response.write('<br><a href=%s>Go Home</a>' %('/') )
			

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/palli',PallindromeChecker)
], debug=True)








		# elif(self.request.get('check3')):
		# 	n=int(self.request.get('num'))
		# 	temp=n
		# 	a=0
		# 	while(n):
		# 		z=1
	 #      		f=1
	 #      		r=n%10;
	 #      		while(z<=r):
	 #         		f=f*z
	 #         		z=z+1
	 #         	a=a+f
	 #      		n=int(n/10)
	 #      	self.response.write(n)	
	 #      	# if(a==temp):
  #     		# 	self.response.write('The entered number is a strong number')	
  #     		# else:
  #     		# 	self.response.write('The entered number is not a strong number')							




	


