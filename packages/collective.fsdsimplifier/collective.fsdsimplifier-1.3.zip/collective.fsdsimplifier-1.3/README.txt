Introduction
============

This product simplifies FacultyStaffDirectory to make it more friendly to end-users.  
It hides tabs that most users don't need to see when editing their profile
and cleans up some visual clutter.  The options remain visible to Managers and Personnel 
Managers who may need to access them.

In particular, this product will:

* Hide the Contents, Sharing, and Relations tabs from the user (when viewing their Person).

* Hide the Actions and Display menus from the user (when viewing their Person).

* Hide the Employment Information, User Settings, categorization, dates, ownership, and settings schema fields from   the user (when editing their Person).

* Correct the versioning configuration so that the "Save as new version" box
  will not display at the bottom when editing a Person (unless versioning is
  enabled).

* (Plone 3) Make the username in the personal bar link directly to the FSD profile,
  instead of the Plone dashboard (and hide the default FSD 'My Folder' link).
  
* (Plone 4) Rename the FSD 'My Folder' link to 'My Profile' in the personal tools.
  
Installation Notes
------------------
You should install FacultyStaffDirectory first before using this product.  FSD Simplifier will uninstall safely, but the permissions to access the Actions and Display menus on Persons will remain disabled for the user.  This is because Persons are set back to the fsd_person_workflow, where the relevant permissions are not managed.

Compatibility
-------------
Verified to work with:

* Plone 3.3.5 - FSD 2.1.4, 3.0b1, 3.0b2, and 3.0b3
* Plone 4.0.3 - FSD 3.0b3  

It has not been tested with versions of Plone before 3.3.5 or FSD before 2.1.4.  It is likely to be compatible with later versions, but you should test on a development instance first.

Credits
============

This product was first developed by Heather Wozniak during the West Coast Plone Sprint 2010 organized by the Los Angeles Plone Users Group (http://laplone.org).  

Special thanks to Alec Mitchell and Luke Brannon for their guidance and assistance with this project.  And to the WebLion group at Penn State University for developing the great FacultyStaffDirectory.
