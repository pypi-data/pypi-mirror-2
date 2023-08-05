broken_since is a nose plugin, nose is a alternate test discovery and running
process for unitest 

author: Francis Pieraut 2009 francis@qmining.com

broken_since is:
1) defining broken_since(version, user, reason) decorator that is deactivating
a unittest and display a warning instead. 
2) add option --broken-since to get a summary report at the end of nosetests 
call. 
========================================================================

To get more detail about nose, follow this link:
http://somethingaboutorange.com/mrl/projects/nose/

Licence
-------
not at this point 

Instructions
------
1) install nose (easy_install nose)
2) install pluging (python setup.py install)
3) try it: nosetests --broken-since

To desactivate a broken unittest, add the broken_since decorator like this:

@broken_since(version='x.x.x', user='fpieraut', reason='no ssl key')
def test_do_something_great():
    ...

