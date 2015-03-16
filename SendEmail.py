import logging
from datetime import datetime
import webapp2
import jinja2
from google.appengine.api import mail, users
from SubscriptionStore import SubscriptionGroupModel

APP_EMAIL = 'anthonykleiser@gmail.com'
DAYS = {
    0: 'monday_content',
    1: 'monday_content',
    2: 'wednesday_content',
    3: 'thursday_content',
    4: 'friday_content',
    5: 'saturday_content',
    6: 'sunday_content',
}

class SendEmail(webapp2.RedirectHandler):
    def get(self):
        user = users.get_current_user()
        day = DAYS[datetime.today().weekday()]

        if user is not None:
            user_email = user.email()
            query = SubscriptionGroupModel.query(
                SubscriptionGroupModel.subscriber_id == user.user_id())
            current_subscription_group = query.get()
            query_day = 'current_subscription_group.' + day
            daily_links = eval(query_day)
            




            message = ''

            template_values = {
                'message': message
            }

        self.redirect('/')