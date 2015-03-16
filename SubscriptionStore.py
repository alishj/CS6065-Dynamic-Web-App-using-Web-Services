import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb


class SubscriptionGroupModel(ndb.Model):
    subscriber_id = ndb.StringProperty(indexed=True)
    subscriber_email = ndb.StringProperty(indexed=False)
    monday_content = ndb.StringProperty(indexed=False)
    tuesday_content = ndb.StringPropery(indexed=False)
    wednesday_content = ndb.StringProperty(indexed=False)
    thursday_content = ndb.StringProperty(indexed=False)
    friday_content = ndb.StringProperty(indexed=False)
    saturday_content = ndb.StringProperty(indexed=False)
    sunday_content = ndb.StringProperty(indexed=False)


class Subscribe(webapp2.RequestHandler):
    def post(self):
        # Get current user
        user = users.get_current_user()

        if user and not user.user_id() is None:
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
                current_subscription_group.monday_content += ';'.append(site)
            if self.request.get('tue') == 'Tuesday':
                current_subscription_group.tuesday_content += ';'.append(site)
            if self.request.get('wed') == 'Wednesday':
                current_subscription_group.wednesday_content += ';'.append(site)
            if self.request.get('thu') == 'Thursday':
                current_subscription_group.thursday_content += ';'.append(site)
            if self.request.get('fri') == 'Friday':
                current_subscription_group.friday_content += ';'.append(site)
            if self.request.get('sat') == 'Saturday':
                current_subscription_group.saturday_content += ';'.append(site)
            if self.request.get('sun') == 'Sunday':
                current_subscription_group.sunday_content += ';'.append(site)

            current_subscription_group.put()
            self.redirect('/subscribeform')
        elif not user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('<a href="%s">Sign in</a>' % users.create_login_url('/'))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Please <a href=%s>sign in</a> with a Google account' % users.create_login_url('/'))