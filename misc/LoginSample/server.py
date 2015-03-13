import webapp2
from google.appengine.api import users

def getHTML():
    f = open("HelloWorld.html", 'r')
    return f.read()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(getHTML())

        
def getFoo():
    f = open("Foo.html", 'r')
    return f.read()
    
class Foo(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and not user.user_id() == None:
            print "User id: " + user.user_id()
            self.response.headers['Content-Type'] = 'text/html'
            html = (getFoo() % (users.create_logout_url('/Foo/'),user.nickname() + " logout"))
            self.response.write(html)
        elif not user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<a href=%s>Sign in</a>' % users.create_login_url('/Foo/'))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Please <a href=%s>sign in</a> with a Google account' % users.create_login_url('/Foo/'))
            
        
application = webapp2.WSGIApplication([
    ('/', MainPage),('/Foo/', Foo)], debug=True)