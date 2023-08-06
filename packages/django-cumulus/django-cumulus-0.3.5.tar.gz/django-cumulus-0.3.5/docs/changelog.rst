changelog
=========

Version 0.3.5, 07 January 2011
******************************

* Fixed glaring issue affecting Django > 1.1.x (see http://bit.ly/e8YhcR)
* Removed reliance on physical files for tests
* Added tox config to test multiple versions of Python and Django

Version 0.3.4, 13 September 2010
********************************

* Reverted exception handling to pre-2.6 style
* Added example project to repo

Version 0.3.3, 12 July 2010
***************************

* Removed reliance on bitbucket tag download files

Version 0.3.2, 12 July 2010
***************************

* Pulled in Ian Schenck's delete_object fix

Version 0.3.1, 18 May 2010
**************************

* Fixed syncstatic deletion bug
* Require verbosity > 1 for syncstatic output

Version 0.3, 17 May 2010
**************************

* Added syncstatic management command

Version 0.2.3, 03 May 2010
**************************

* Fix bug when accessing imagekit attributes
* Fix setup.py distribute installation issue

Version 0.2.2, 11 February 2010
*******************************

* Fixed bug when using django-imagekit

Version 0.2, 10 February 2010
*****************************

* Changed focus and aim of project
* Removed all previous custom admin work
* Incorporated CloudFilesStorage custom storage backend
* Added sphinx docs
* Converted setup to use distribute

Version 0.1, 28 July 2009
*************************

* Initial release
