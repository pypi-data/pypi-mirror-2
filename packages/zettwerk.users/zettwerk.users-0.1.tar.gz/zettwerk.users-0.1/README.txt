Introduction
============

At the point of writing, zettwerk.users provides an additional view /@@userlist_view. This view can be found via the plone controlpanel "Zettwerk Users".
It lists the users, available in your plone instance, and shows your wether the user already logged in or not. You can select all users that did not log in yet and reset their passwords. However, it is also possible to select single users by hand.

You can filter the users by groups. By default, all users are shown.

Installation
============

Just put zettwerk.users into your buildout.cfg

  [instance]
  ...
  eggs += zettwerk.users
  zcml += zettwerk.users
  ...

Use the portal_quickinstaller to register the "Zettwerk Users" to the controlpanel.
