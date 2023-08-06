
newsletter contains a library for newsletters and a newsletterapp


Install newsletter with virtualenv and pip
==========================================

This makes an isolated install for you, so it does not pollute your system packages.

.. code-block:: bash

	virtualenv --no-site-packages --distribute myvirtualpython
	cd myvirtualpython
	source bin/activate
	pip install newsletter
	newsletterapp --help

Installing with virtualenv and pip is recommended.

Install newsletter with ./configure; make
=========================================

This is for old school unix peoples.

.. code-block:: bash

	./configure; make

Install newsletter with setup.py
================================

python setup.py install



