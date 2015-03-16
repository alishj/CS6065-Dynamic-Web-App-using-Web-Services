import webapp2
import logging

from google.appengine.api import users
from google.appengine.ext import ndb


class SubscriptionGroupModel(ndb.Model):
    subscriber_id = ndb.StringProperty(indexed=True)
    subscriber_email = ndb.StringProperty(indexed=False)
    monday_content = ndb.StringProperty(indexed=False)
    tuesday_content = ndb.StringProperty(indexed=False)
    wednesday_content = ndb.StringProperty(indexed=False)
    thursday_content = ndb.StringProperty(indexed=False)
    friday_content = ndb.StringProperty(indexed=False)
    saturday_content = ndb.StringProperty(indexed=False)
    sunday_content = ndb.StringProperty(indexed=False)


class Unsubscribe(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and user.user_id() is not None:
            query = SubscriptionGroupModel.query(
                SubscriptionGroupModel.subscriber_id == user.user_id()
            )
            current_subscription_group = query.get()
            if current_subscription_group is not None:
                current_subscription_group.key.delete()
            self.redirect('/')
        elif not user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<a href="%s">Sign in</a>' % users.create_login_url('/'))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Please <a href=%s>sign in</a> with a Google account' % users.create_login_url('/'))


class Subscribe(webapp2.RequestHandler):
    def post(self):
        # Get current user
        user = users.get_current_user()

        if user and user.user_id() is not None:
            # Check for existing user sub entry, if one does not exist
            # then create a new subscription model entry for them.
            query = SubscriptionGroupModel.query(
                SubscriptionGroupModel.subscriber_id == user.user_id()
            )
            current_subscription_group = query.get()
            if current_subscription_group is None:
                current_subscription_group = SubscriptionGroupModel(
                    subscriber_id=user.user_id(),
                    subscriber_email=user.email()
                )

            # Store email subscription
            site=self.request.get('site')
            if self.request.get('mon') == 'Monday':
                if current_subscription_group.monday_content is None:
                    current_subscription_group.monday_content = site
                else:
                    current_subscription_group.monday_content = str(current_subscription_group.monday_content)+';'+site
                logging.debug("Monday content: %s", str(current_subscription_group.monday_content))
            if self.request.get('tue') == 'Tuesday':
                if current_subscription_group.tuesday_content is None:
                    current_subscription_group.tuesday_content = site
                else:
                    current_subscription_group.tuesday_content = str(current_subscription_group.tuesday_content)+';'+site
                logging.debug("Tuesday content: %s", str(current_subscription_group.tuesday_content))
            if self.request.get('wed') == 'Wednesday':
                if current_subscription_group.wednesday_content is None:
                    current_subscription_group.wednesday_content = site
                else:
                    current_subscription_group.wednesday_content = str(current_subscription_group.wednesday_content)+';'+site
                logging.debug("Wednesday content: %s", str(current_subscription_group.wednesday_content))
            if self.request.get('thu') == 'Thursday':
                if current_subscription_group.thursday_content is None:
                    current_subscription_group.thursday_content = site
                else:
                    current_subscription_group.thursday_content = str(current_subscription_group.thursday_content)+';'+site
                logging.debug("Thursday content: %s", str(current_subscription_group.thursday_content))
            if self.request.get('fri') == 'Friday':
                if current_subscription_group.friday_content is None:
                    current_subscription_group.friday_content = site
                else:
                    current_subscription_group.friday_content = str(current_subscription_group.friday_content)+';'+site
                logging.debug("Friday content: %s", str(current_subscription_group.friday_content))
            if self.request.get('sat') == 'Saturday':
                if current_subscription_group.sunday_content is None:
                    current_subscription_group.saturday_content = site
                else:
                    current_subscription_group.saturday_content = str(current_subscription_group.saturday_content)+';'+site
                logging.debug("Saturday content: %s", str(current_subscription_group.saturday_content))
            if self.request.get('sun') == 'Sunday':
                if current_subscription_group.sunday_content is None:
                    current_subscription_group.sunday_content = site
                else:
                    current_subscription_group.sunday_content = str(current_subscription_group.sunday_content)+';'+site
                logging.debug("Sunday content: %s", str(current_subscription_group.sunday_content))

            current_subscription_group.put()
            self.redirect('/Subscribeform')
        elif not user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<a href="%s">Sign in</a>' % users.create_login_url('/'))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Please <a href=%s>sign in</a> with a Google account' % users.create_login_url('/'))