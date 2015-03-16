import webapp2
from google.appengine.api import mail

def get_main_html():
    f = open("MAIN_PAGE_HTML.html", "r")
    return f.read()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        html = get_main_html()
        self.response.write(html)

class SendEmailRedirect(webapp2.RequestHandler):
    def get(self):
        user_address = self.request.get('email')
        # Check if valid email
        if not mail.is_email_valid(user_address):
            self.response.write('Please enter a valid email')
        else:
            sender_address = "Email-sample.appspotmail.com Support <support@email-sample.appspotmail.com>"
            subject = "Notify Email"
            body = "This email will eventually come with information. Just not now."
            mail.send_mail(sender_address, user_address, subject, body)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<html><body><p>Sending email to <i>' + user_address)
            self.response.write('</i></p></body></html>')
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/notify', SendEmailRedirect),
],debug=True)