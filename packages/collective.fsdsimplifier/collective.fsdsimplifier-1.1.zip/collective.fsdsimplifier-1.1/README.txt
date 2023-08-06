Introduction
============

This product simplifies FacultyStaffDirectory to make it more user-friendly.  
It hides tabs that most users don't need to see when editing their profile
and cleans up some visual clutter.  The options remain visible to Managers and Personnel 
Managers who may need to access them.

In particular, this product will:

* Hide the Contents, Sharing, and Relations tabs from the user (when viewing their Person).

* Hide the Actions and Display menus from the user (when viewing their Person).

* Hide the User Settings, categorization, dates, ownership, and settings schema from the user
  (when editing their Person).

* Correct the versioning configuration so that the "Save as new version" box
  will not display at the bottom when editing a Person (unless versioning is
  enabled).

* Make the username in the personal bar link directly to the FSD profile,
  instead of the Plone dashboard (and hide the default FSD 'My Folder' link).
  
Installation Notes
------------------
You should install FacultyStaffDirectory first before using this product.  It was developed and tested with Plone 3.3.5 and FSD 2.1.4.

Version 1.1 will uninstall safely, but a few settings are left behind.  The permissions to access the Actions and Display menus will remain disabled and the hidden schema will remain hidden (working on undoing this for next release).

Credits
============

This product was developed by Heather Wozniak during the West Coast Plone Sprint 2010 organized by the Los Angeles Plone Users Group (http://laplone.org).  

Special thanks to Alec Mitchell and Luke Brannon for their guidance and assistance with this project.  And to the WebLion group at Penn State University for developing the great FacultyStaffDirectory.
