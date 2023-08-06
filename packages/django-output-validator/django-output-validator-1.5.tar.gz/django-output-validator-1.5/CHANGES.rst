Changelog
=========

Version 1.5 - 2010-12-01
------------------------

* Re-branded as django-output-validator and packaged properly.

  If you used the previous version, you should drop the old
  'validator_validationfailure' table (assuming it doesn't have any data you
  need, of course). Then go through the installation instructions in the README
  and update the name/values of the relevant settings.

* Fixed stashing of request objects (now uses repr). This is BACKWARDS
  INCOMPATIBLE with existing data (but we are using a new table anyway).


Version 1.4 - 2008-04-28
------------------------

* Changed maxlength to max_length, as per change in Django.
* Corrections to instructions (thanks to Gary Wilson)
* Fixed deprecation warnings (thanks to Gary Wilson)


Version 1.3 - 2007-11-05
------------------------

* Updated for unicodisation of Django.

  This is a BACKWARDS INCOMPATIBLE change.

  The problem was caused by the fact that you used to able to store arbitrary
  binary data in a TextField, which is no longer possible. As a result, I am
  using base64 encoding for any pickled objects. I haven't written an upgrade
  script for the database (since I personally keep the list of failed pages to
  zero). If you are upgrading from a previous version, any of your existing
  ValidationFailure objects will be corrupted (the 'request' and 'response' data
  will be lost). Either deal with the errors before upgrading, or write a
  conversion script of some kind :-)

Version 1.2 - 2007-04-18
------------------------

* Fixed bug that occurred when settings.VALIDATOR_APP_IGNORE_PATHS wasn't set
* Added logic to stop duplicate failures being logged

Version 1.1 - 2005-12-14
------------------------

* Added optional VALIDATOR_APP_IGNORE_PATHS setting.
* Added support for mod_python handler - thanks to 'nesh'.
* Added a setup.py script.

Version 1.0 - 2005-11-19
------------------------
* Initial release
