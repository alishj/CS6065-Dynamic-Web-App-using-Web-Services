import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_SUBGROUP_NAME = 'default_group'

def group_key(group_name=DEFAULT_SUBGROUP_NAME):
    return ndb.Key('Subgroup', group_name)

class SubscriptionGroup(ndb.Model):
    author_id = ndb.StringProperty(indexed=True)
    author_email = ndb.StringProperty(indexed=False)
    monday_content = ndb.StringProperty(indexed=False)
    tuesday_content = ndb.StringProperty(indexed=False)
    wednesday_content = ndb.StringProperty(indexed=False)
    thursday_content = ndb.StringProperty(indexed=False)
    friday_content = ndb.StringProperty(indexed=False)
    saturday_content = ndb.StringProperty(indexed=False)
    sunday_content = ndb.StringProperty(indexed=False)

def getMainHTML():
    f = open('MAIN_PAGE_HTML.html', 'r')
    return f.read()

def getSubHTML():
    f = open('FORM_SUBMIT_HTML.html', 'r')
    return f.read()

# This is called when a subscription form is submitted.
class SubscribeStore(webapp2.RequestHandler):
    def post(self):
        # Save the user's id, email, and assign the website
        # for whatever day they had checked.
        # TODO: Allow multiple websites per entry.
        group_name = DEFAULT_SUBGROUP_NAME
        qry = SubscriptionGroup.query(SubscriptionGroup.author_id==str(users.get_current_user().user_id()))
        subscription_model = qry.get()
        
        site = self.request.get('site')
        if self.request.get('mon') == 'Monday':
            subscription_model.monday_content = site
        if self.request.get('tue') == 'Tuesday':
            subscription_model.tuesday_content = site
        if self.request.get('wed') == 'Wednesday':
            subscription_model.wednesday_content = site
        if self.request.get('thu') == 'Thursday':
            subscription_model.thursday_content = site
        if self.request.get('fri') == 'Friday':
            subscription_model.friday_content = site
        if self.request.get('sat') == 'Saturday':
            subscription_model.saturday_content = site
        if self.request.get('sun') == 'Sunday':
            subscription_model.sunday_content = site
        # Write the data to the datastore
        subscription_model.put()
        html = (getSubHTML() % (self.request.get('id')))
        self.response.write(html)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            # Make a query for the current user's id and fetch the result.
            # The purpose of this current_sub is to show the user what websites
            # they are subscribed to and what days they are receiving these
            # updates.
            # TODO: Allow multiple websites to be shown for each day.
            #       Implement current_sub.monday_content (and a similar
            #         call for all other days).
            qry = SubscriptionGroup.query(SubscriptionGroup.author_id==str(user.user_id()))
            current_sub = qry.get()
            self.response.headers['Content-Type'] = 'text/html'
            html = (getMainHTML() % (user.nickname(), current_sub.monday_content,
                current_sub.tuesday_content, current_sub.wednesday_content,
                current_sub.thursday_content, current_sub.friday_content,
                current_sub.saturday_content, current_sub.sunday_content,
                user.user_id()))
            self.response.write(html)
        else:
            self.redirect(users.create_login_url(self.request.uri))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/subscribe', SubscribeStore),
],debug=True)
