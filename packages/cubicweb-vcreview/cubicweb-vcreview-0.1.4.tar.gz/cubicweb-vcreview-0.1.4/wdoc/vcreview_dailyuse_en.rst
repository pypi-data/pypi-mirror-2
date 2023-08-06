
Naming patches
~~~~~~~~~~~~~~
Think to name you patch with '.diff' extension, else you won't see the diff
until you've fixed the file's content type through "modify". Also, notice
the following points:

* for commit message magic words explained below to work, patch name should
  match the regular expression '[-\.\w]+'

* patch renaming should be correctly followed, but shouldn't be anymore
  necessary to mark patch as in-progress, pending review, etc... : you've
  an application for that now!

* patches should be kept isolated in the branch they have been created in,
  else you may have multiple patch entities created for something that is
  actually a single patch


Submit a patch for review
~~~~~~~~~~~~~~~~~~~~~~~~~
You can either do it regularly through the web ui, or by having: ::

  "<patch path> ready for review"

on a line of the patch repository commit message. This will change the
patch'state to 'pending-review'.


Accepting a patch
~~~~~~~~~~~~~~~~~
You can either do it regularly through the web ui, or by having: ::

  "applied <patch path>"

on a line of the patch repository commit message. This will change the
patch'state to 'applied'.


Rejecting a patch
~~~~~~~~~~~~~~~~~
You can either do it regularly through the web ui, or by having: ::

  "reject <patch path>"

on a line of the source repository commit message. This will change the
patch'state to 'rejected'.


Folding a patch
~~~~~~~~~~~~~~~
When a patch is folded into another one, it should be marked as 'folded'.
You can either do it regularly through the web ui, or by having: ::

  "fold <patch path>"

on a line of the source repository commit message. This will change the
patch'state to 'folded'.


Notification
~~~~~~~~~~~~
To be notified about patches activity, you should mark yourself as 'interested
in' each desired patch repository.

