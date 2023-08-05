INSTALLING
==========

Stable releases can be installed with pip and using
virtualenv is recommended::

	% virtualenv myenv
	% . ./myenv/bin/activate
	(myenv)% pip install ordf

Development branch, do instead::

	(myenv)% pip install mercurial
	(myenv)% pip install -e hg+http://ordf.org/src#egg=ordf

That should install everything required. If you would like
to use the message passing facilities, you will need to 
install 'carrot'::

	(myenv)% pip install carrot

TESTING
=======

To run tests::

	(myenv)% pip install nose
	(myenv)% cd myenv/src/ordf
	(myenv)% python setup.py nosetests --verbosity=2 -s

*NOTE*: to run the fourstore tests you need to have a
4store instance serving a kb called ordf_test. To do
this::

	% 4s-backend-setup ordf_test
	% 4s-backend ordf_test

Also make sure to install py4s from http://github.com/wwaites/py4s
This requires at least version 0.8
Also see http://wiki.github.com/wwaites/py4s/installing-py4s

*NOTE*: to run the rabbitmq tests, rabbitmq-server needs to
be running with an exchange ordf_test that can be accessed
by the user guest/guest.


DOCUMENTATION
=============

To build the docs,

	(myenv)% pip install sphinx
	(myenv)% python setup.py build_sphinx

and the documentation will be in */build/sphinx/html/index.html*
