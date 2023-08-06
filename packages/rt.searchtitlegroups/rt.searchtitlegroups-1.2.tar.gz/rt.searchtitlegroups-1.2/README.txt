Introduction
============

This product allow to search in titles and ids of groups of Pone3.
To do this we have done some changes at Plone's functionality.

First of all we have fixed an error in the updateGroup procedure to save in the correct way the user in Zope.
To do this we have patched Products.PlonePAS like Plone4 does.
Connected to this we have modified the prefs_group_edit script. 
The modify is necessary to keep updated the groups in Zope when the users modifies the groups by the Plone form.

To modify the search functionality we have create a view that does two search into the groups: 
one in the id and one in the title.
We go to use the new view for search into the manage of groups of Plone (plone control panel) and sharing tab.
