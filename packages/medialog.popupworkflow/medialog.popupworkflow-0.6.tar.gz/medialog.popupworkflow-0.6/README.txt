What is this?
=============

This Plone product gives you a new'popup_workflow so you can "publish an item for pop-up effect when clicking on it in the navigation menu or wherever the state class  is shown (like in folder_listing, tableview, )
The popup effect is disabled when logged in (so its possible to edit content "the normal way")


How-to
==================
- Install collective.prettyphoto
- Install medialog.popupworkflow (in that order)
- Change workflow of a folder or content type or everything to "Popup workflow"
- Supported content types: folder (collective.gallery, Product.Maps, collective.truegallery), FormFolder, Page)
- "Change state of some content to Popup Publish". For security reasons, the "change view menu is now disabled". You will need to "Normal Publish" it to change view.
ÐÊLog out, or use another browser
- Click on that item in the navigation portlet

If you uninstall the product, you should uninstall or reinstall collective.prettyphoto


Credits
====
Nathan van Gheem, whose products and help inspired me to make this.


Authors
=======

This product was developed by Espen Moe-Nilssen espen at medialog dot no