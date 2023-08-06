Introduction
============
collective.piwik.now displays a portlet with the number of users currently using your Plone site.

The Piwik open source analytics system (http://piwik.org/) is used to store the usage data.

How to get it working
=====================

 - You need to have access to a working Piwik installation. Create a new site in the Piwik admin UI and provide the view permission to anonymous users.

 - Add the Piwik Tracking Tag to Javascript web stats support field at <SITEURL>/@@site-controlpanel

 - You need to make a small change at the tracking tag adding the line "var site_id = X;", replacing X with your Piwik site_id
   For example, if in the Piwik code you have:
   var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php", 6);
   then site_id = 6 in your case

 - Install the "Online users" add-on from the Plone control panel

 - Add the "Online users" portlet from the manage portlets form in the context you want it to appear. At this step you can configure the session timeout in minutes: The time of inactivity after which a user is no longer considered to be online.


Credits
=======

The product was created by Unweb.me during the Bristol 2010 Plone conference.
Thanks to Engagemedia.org for sponsoring our tickets and registrations.
