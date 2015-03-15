import webapp2
import cgi
from google.appengine.api import users

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

class Subscribe(webapp2.RequestHandler):
    def getHTML(self):
        f = open('Subscribe.html', 'r')
        return f.read()

    def post(self):
        user = users.get_current_user()
        if user and not user.user_id() == None:
            self.response.headers['Content-Type'] = 'text/html'
            html = (self.getHTML() % (user.user_id(), self.request.get('site'), self.request.get('mon'), self.request.get('tue'),
                    self.request.get('wed'), self.request.get('thu'), self.request.get('fri'), self.request.get('sat'), self.request.get('sun')))
            self.response.write(html)
        else:
            self.redirect('/Logout')
            
class MainPage(webapp2.RequestHandler):
    def getHTML(self):
        f = open('Main.html', 'r')
        return f.read()

    
        
    def get(self):
        user = users.get_current_user()
        if user and not user.user_id() == None:
            html = (self.getHTML() % (user.nickname(), users.create_logout_url('/Logout')))
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(html)
        elif not user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<a href="%s">Sign in</a>' % users.create_login_url('/'))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Please <a href=%s>sign in</a> with a Google account' % users.create_login_url('/'))
        


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Logout', LogoutPage),
    ('/Subscribe', Subscribe),
],debug=True)