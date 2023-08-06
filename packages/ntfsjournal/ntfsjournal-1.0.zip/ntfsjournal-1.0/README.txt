pyntfsjournal v1.0
-----------------------------

Website: http://pyntfsjournal.sourceforge.net/
Developed by: Lazar Laszlo
Contact: laszlolazar@yahoo.com

Released under GPL 3.0 see gpl-3.0.txt.

Installation

If you have downloaded and unzipped the package then you need to run the
"setup.py" script with the "install" argument::

     python setup.py install

This should put ``ntfsjournal.pyd`` in your ``site-packages`` directory. 

Example:

import ntfsjournal
ntfsjournal.get('c', ntfsjournal.USN_REASON_FILE_DELETE)

The above script will get the delete journal for drive C.

Other filters:

ntfsjournal.USN_REASON_ALL
ntfsjournal.USN_REASON_CLOSE
ntfsjournal.USN_REASON_DATA_EXTEND
ntfsjournal.USN_REASON_DATA_OVERWRITE
ntfsjournal.USN_REASON_EA_CHANGE
ntfsjournal.USN_REASON_FILE_CREATE
ntfsjournal.USN_REASON_FILE_DELETE
ntfsjournal.USN_REASON_HARD_LINK_CHANGE
ntfsjournal.USN_REASON_RENAME_NEW_NAME
ntfsjournal.USN_REASON_RENAME_OLD_NAME
ntfsjournal.USN_REASON_SECURITY_CHANGE
