import os
import jinja2
import webapp2
import datetime
from SubscriptionStore import Subscribe
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class LogoutPage(webapp2.RequestHandler):
    def getHTML(self):
        f = open('Logout.html', 'r')
        return f.read()
        
    def get(self):
        user = users.get_current_user()
        if user and not user.user_id() == None:
            self.redirect('/')
        else:
            html = (self.getHTML() % users.create_login_url('/'))
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(html)

class SendMail(webapp2.RequestHandler):
    def sendEmail(self):
        # TODO: Add functionality to send emails based on 
        return True

    def getMail(self, user, date):
        # TODO: Add functionality to query database for email information
        return True

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<h1>FUNCTIONALITY TO BE ADDED</h1>')
        
            
class ForceMail(SendMail):
    def post(self):
        user = users.get_current_user()
        if user and not user.user_id() == 'None':
            # The weekday returns the day of the week from 0-6 Mon-Sun respectively
            self.getMail(user.user_id(), datetime.datetime.today().weekday())
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<h1>Today's numeric date is: %s</h1>" % datetime.datetime.today().weekday())
        else:
            self.redirect('/Logout')


class SubscribeForm(webapp2.RequestHandler):
    def getHTML(self):
        f = open('Subscribe_Form.html', 'r')
        return f.read()

    def get(self):
        user = users.get_current_user()
        if user and user.user_id() is not None:
            self.response.headers['Content-Type'] = 'text/html'
            html = self.getHTML()
            self.response.write(html)
        else:
            self.redirect('/Logout')

            
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and user.user_id() is not None:
            template_values = {
                'nickname': user.nickname(),
                'logout_url': users.create_logout_url('/Logout')
            }
            template = JINJA_ENVIRONMENT.get_template('Main.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Logout', LogoutPage),
    ('/Subscribeform', SubscribeForm),
    ('/Subscribe', Subscribe),
    ('/Forcemail', ForceMail),
    ('/Sendemail', SendMail)
],debug=True)