import os
import jinja2
import webapp2
import datetime
from SubscriptionStore import Subscribe, Unsubscribe
from google.appengine.api import users
from SendEmail import SendEmail


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class LogoutPage(webapp2.RequestHandler):
        
    def get(self):
        user = users.get_current_user()
        if user and user.user_id() is not None:
            self.redirect('/')
        else:
            template_values = {
                'login_url': users.create_login_url('/')
            }
            template = JINJA_ENVIRONMENT.get_template('Logout.html')
            self.response.write(template.render(template_values))


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
            self.redirect(users.create_login_url())


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Logout', LogoutPage),
    ('/Subscribeform', SubscribeForm),
    ('/Unsubscribe', Unsubscribe),
    ('/Subscribe', Subscribe),
    ('/Forcemail', SendEmail)
],debug=True)