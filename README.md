CloudComputingP3
================

Dynamic Web App using Web Services or NoSQL

*Anthony Kleiser, Chris McVeigh, Sean Schatzman*

### Description
A web service hosted on Google's App Engine platform that allows users to create subscriptions containing url links that will be sent to them on the days they specify. Users log in with their Google account, enter urls into a form field, and select the days they want to receive their subscriptions. Each user's subscriptions are stored using Google's Datastore service. Subscription urls can then be sent to their Google email.

### Services Used (Within Google App Engine)
- Users
- Datastore
- Mail

### Possible Future Work
- A backend server that regularly checks the date and sends subscriptions accordingly.
- Ability for users to remove individual urls from their subscriptions.
- Ability for users to share their subscriptions.