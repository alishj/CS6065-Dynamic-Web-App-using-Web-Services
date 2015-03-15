import webapp2
import cgi
from google.appengine.api import users

def getMainHTML():
    f = open('MAIN_PAGE_HTML.html', 'r')
    return f.read()

def getSubHTML():
    f = open('FORM_SUBMIT_HTML.html', 'r')
    return f.read()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html'
            html = (getMainHTML() % (user.nickname(), user.user_id()))
            self.response.write(html)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class SubPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        html = (getSubHTML() % (self.request.get('id'), self.request.get('site'), self.request.get('day')))
        self.response.write(html)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/subscribe', SubPage),
],debug=True)
