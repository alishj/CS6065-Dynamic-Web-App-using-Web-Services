import webapp2
import jinja2
from google.appengine.api import mail, app_identity

APP_EMAIL = 'anthonykleiser@gmail.com'

class SendEmail(webapp2.RedirectHandler):
    def post(self):
        user_address = self.request.get('email')
        message = ''
        if not mail.is_email_valid(user_address):
            message = 'Please enter a valid email.'
        else:
            subject = 'Subscription Confirmation'
            body = ''

        template_values = {
            'message': message
        }