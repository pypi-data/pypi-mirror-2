What is this?
=============

This Plone product gives you a new'popup_workflow. 
Its basically the simple publication workflow with one weird extra: It lets you "publish an item for pop-up effect when clicking on it in the navigation menu

What is this for
==================
The idea is that a user (with the right permissions) can decide if he wants to show something as an overlay or as a normal page. 
 
1) Make a new workflow state and if the page/folder has this state it will open in an overlay instead of as a normal plone page


How-to
==================
- Install collective.prettyphoto
- Install medialog.popupworkflow (in that order)
- Change workflow of a folder or content type to "Medialog Popup workflow"
- "Change state of some content to Popup Publish"
- go to /portal_types in zmi and add alias for the view you want to use, for example
[place] [@galleryplaceview] ..... I am working on fixing this step... help welcome
- Click on that item in the navigation portlet


The only view avalable for this at the moment is for collective.truegallery and collective.gallery and maps (works with both folder and location, but you will have to go to portal_skins/popuworkflow and customize it for now...)



TODO
====
I am doing some thinking (and asking) about how to make a generic view for popups. Hopefully this is doable.


Need tests!

Credits
====
kiorky, help with variables in js
Nathan van Gheem always helpful

Authors
=======

This product was developed by Espen Moe-Nilssen espen at medialog dot no