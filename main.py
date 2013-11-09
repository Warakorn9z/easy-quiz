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
#

import webapp2
import os
import jinja2
from google.appengine.api import rdbms
from google.appengine.api import users
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.ext.webapp import template
from gaesessions import get_current_session
from gaesessions import SessionMiddleware
from login import Login

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

INSTANCE_NAME = "gcdc2013-easyquiz:quiz1"
DATABASE = "quizdb"

decorator = OAuth2Decorator(
	client_id='981805140817.apps.googleusercontent.com',
        client_secret='YT2KhOg3nPgXUeV60wA3iAwS',
	scope='https://www.googleapis.com/auth/drive'
)

service = build('drive', 'v2')

class Main(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {
			'username' : users.get_current_user()
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/index.html')
		self.response.write(get_template.render(templates))

class CreateQuiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {
			'username' : users.get_current_user()		
		}
		get_template = JINJA_ENVIRONMENT.get_template('templates/add.html')
		self.response.write(get_template.render(templates))

class CreateQuizHandler(webapp2.RequestHandler):
	@decorator.oauth_required
   	def post(self):
		title = self.request.get('title')
		description = self.request.get('description')
		start_date = self.request.get('start_date')
		end_date = self.request.get('end_date')
		location = self.request.get('location')
		self.response.write("Hello: " + title + ", " + description)
		con = rdbms.connect(instance=INSTANCE_NAME, database=DATABASE)
    		cursor = con.cursor()
        	sql="insert into Quiz (title, description, start, end, address) values ('%s', '%s', '%s', '%s', '%s')"%(title, description, start_date, end_date, location)
    		cursor.execute(sql)
		con.commit()
		con.close()

class Quiz(webapp2.RequestHandler):
	@decorator.oauth_required
   	def get(self):
        	templates = {			
		}
		get_template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(get_template.render(templates))


app = webapp2.WSGIApplication([
    	('/', Main),
	('/Create', CreateQuiz),
	('/CreateQuizHandler', CreateQuizHandler),
	(decorator.callback_path, decorator.callback_handler())
], debug=True)
app = SessionMiddleware(app, cookie_key=str(os.urandom(64)))
