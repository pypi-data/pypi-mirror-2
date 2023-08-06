=== ABOUT ===
This library implements all features of the RestAuth specification and is a
reference implementation. It is written in pure python. It generally works with
python 2.6 or later (including python3). 

=== INSTALLATION ===
The library ships with a with a standard setup.py file, so you should be able to
install it with a simple

	python setup.py install

If you want to install the library in python 3.x, you probably need to invoke
the setup.py with python3:

	python3 setup.py install

===== On Debian/Ubuntu =====
There is an APT repository providing debian packages for all restauth software.
Please see

        https://redmine.fsinf.at/projects/restauth/wiki/APT_repositories

for more information on how to add the repository to your system.

The packages for this library are called python-restauth (for python2.6),
python3-restauth and python-restauth-doc.

=== HOW TO USE ===
The library includes extensive library documentation. If you have sphinx
installed, you can generate it using setup.py:
	
	python setup.py build_doc

... which will create the files in the doc directory. The documentation is also
available online, please see:

	https://python.restauth.net

The examples directory includes a few examples, which you need to invoke from
the top-level directory.
