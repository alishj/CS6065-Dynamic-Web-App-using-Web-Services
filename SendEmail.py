import logging
from datetime import datetime
import webapp2
import jinja2
from google.appengine.api import mail, users
from SubscriptionStore import SubscriptionGroupModel

APP_EMAIL = 'anthonykleiser@gmail.com'
DAYS = {
    0: 'monday_content',
    1: 'tuesday_content',
    2: 'wednesday_content',
    3: 'thursday_content',
    4: 'friday_content',
    5: 'saturday_content',
    6: 'sunday_content',
}

class SendEmail(webapp2.RedirectHandler):
    """
    Retrieves the current user and queries the Subscription datastore based on user_id.
    An email is sent to the user containing the urls they are subscribed to for the current day.
    """
    
    def getHTML(self):
        f = open("No_Subscriptions.html")
        return f.read()

    def get(self):
        user = users.get_current_user()
        day = DAYS[datetime.today().weekday()]

        if user is not None:
            user_email = user.email()
            query = SubscriptionGroupModel.query(
                SubscriptionGroupModel.subscriber_id == user.user_id())
            current_subscription_group = query.get()
            if current_subscription_group is None:
                self.response.headers['Content Type'] = 'text/html'
                self.response.write(self.getHTML())
            else:
                # Create string to use in eval
                query_day = 'current_subscription_group.' + day
                # Queries datastore for the current day's links
                daily_links = str(eval(query_day)).replace(';', '\n')

                subject = 'Your Daily Subscription'
                body = 'Your content for the day is...\n' + daily_links
                mail.send_mail(APP_EMAIL, user_email, subject, body)

                self.redirect('/')
        else:
            self.redirect('/Logout')