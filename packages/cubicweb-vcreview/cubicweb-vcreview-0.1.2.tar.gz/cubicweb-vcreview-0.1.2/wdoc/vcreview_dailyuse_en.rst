
Naming patches
~~~~~~~~~~~~~~
Think to name you patch with '.diff' extension, else you won't see the diff
until you've fixed the file's content type through "modify".


Submit a patch for review
~~~~~~~~~~~~~~~~~~~~~~~~~
You can either do it regularly through the web ui, or by having: ::

  "<patch path> ready for review"

on a line of the patch repository commit message. This will change the
patch'state to 'pending-review'.


Accepting a patch
~~~~~~~~~~~~~~~~~
You can either do it regularly through the web ui, or by having: ::

  "applied patch <patch path>"

on a line of the source repository commit message. This will change the
patch'state to 'applied' and mark the patch as `applied_at` the source repository
revision.


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

