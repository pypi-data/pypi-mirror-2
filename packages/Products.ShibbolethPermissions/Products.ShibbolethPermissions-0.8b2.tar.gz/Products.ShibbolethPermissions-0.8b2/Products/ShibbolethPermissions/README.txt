Overview
========

Extend Plone's folder_localrole_form to grant permissions to Shibboleth users.

*ShibbolethPermissions* replaces the folder_localrole_form with a slightly
modified page that has a Shibboleth section added. The Shibboleth section
depends on configuration made in the ZMI. When configured, when
a new user logs in via Shibboleth, permissions will be granted on existing
objects based on user specified regular expressions.

This doesn't do anything for already existing users that log in via Shibboleth.
Those users can have permissions granted via the regular Plone method, since
they already exist as Plone users.

Requirements
============

* Zope and Plone. Tested with Zope 2.10.11 and Plone 3.3.5

Installation
============

1. Add ``Products.ShibbolethPermissions`` to the eggs-section of your buildout

2. Rerun the buildout.

3. Restart Zope.

4. Install the plugin: Go to your-plone-site -> site setup -> Add/Remove
   Products, and install ShibbolethPermissions.

Using Shibboleth Permissions
============================

For Administrators
------------------

1. In the ZMI, in the acl_users/ShibbolethPermissions's config tab.

2. There are two input areas: the left one lists all Shibboleth attributes that
   will be available to users. Examples are all of the attributes listed in the
   setup and mapping headers. The AutoUserMakerPASPlugin's README.txt has an
   example PHP page that when set up, will show all of the attributes getting
   set by Shibboleth.

3. The right input area is a corresponding list of labels that users see for the
   attributes in the left area. Enter attribute labels in the right input box.

4. Click Save.

When users have granted permissions, the ZMI's options tab will list the
permissions. There will be a checkbox that allows deleting *all* of the rules
for a path. The path will also be a link that the adminstrator can use to
quickly get to the Plone sharing tab, which can be used for individual rule
editting.

For Users
---------

1. In Plone, select the sharing tab on the item you want to share. If you
   don't see a sharing tab, Plone doesn't think you have permissions to do so.

2. In the sharing tab, scroll down to the *Shibboleth Permissions* section. Each
   attribute that has been configured above will be show with an input field.
   Each input field is a Python regular expression. See the python re module at
   http://docs.python.org/lib/module-re.html and *Dive Into Python*'s Regular
   Expressions chapter at http://diveintopython.org/regular_expressions/. Simple
   strings work.

3. Select the role(s) to be granted.

4. Click 'apply settings'.

Once you've set up a rule, Plone will show a 'Manage existing rules' form. In
that, delete a rule or rules by selecting the checkbox to the left of each role
you want to delete, then click 'delete selected shibboleht pattern(s)'.

To modifiy the roles granted by a rule, select the checkbox for a rule, then
select roles to assign, and then click 'assign selected role(s) to selected
shibboleth pattern(s)'.

To change the source values for a rule, create a new rule, then delete the old
one.

Testing
=======

To run the *ShibbolethPermissions* tests, use the standard Zope testrunner:

    $INSTANCE_HOME/bin/zopectl test -s Products.ShibbolethPermissions


Credits
=======

Alan Brenner, of Ithaka Harbors, Inc., under the direction of the Research in
Information Technology program of the Andrew W. Mellon Foundaton, wrote
ShibbolethLogin. I'd like to thank Paul Yuergens of psych.ucla.edu for testing.


Support
=======

For right now, email alan DOT brenner AT ithaka DOT org, or see if I'm on
irc.freenode.net channels #plone, #plone4edu or #weblion as AlanBrenner.
