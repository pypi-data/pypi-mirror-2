Installation
============
   
Requirements
------------

In order to run Wille, you need a Python interpreter:

* Python 2.4 should work, but a version starting from 2.5 is highly recommended
* CPython and Jython have been the most extensively tested
* Python 3 is not supported

Installing Python
-----------------

We recommend using CPython:

* For instructions on obtaning and installing Python, see <http://www.python.org/getit/>.
* Note that Python 3 is not supported!

If you are using Jython <http://www.jython.org/>:

* Make sure you have at least version 2.5.1
* For some Jython specific notes and tips, see section `Running Wille on Jython`.

Installing Wille
----------------

Installing with Easy Install (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have installed setuptools <http://pypi.python.org/pypi/setuptools>, you
can install Wille very conveniently by executing::

	easy_install wille

Installing from a Distribution Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, you can install Wille from its distribution package.

Extract files from the distribution package (.zip) into a temporary folder.
Install Wille by executing the setup file::

	python setup.py install

Verifying Installation
----------------------

Confirm that Wille has been installed by importing it in Python::

	>>> import wille
	>>>

A blank response (above) indicates, the library was successfully loaded. To
verify the installation, you can print out Wille's version::

	>>> wille.__version__
	2.3.0.final.0 

Depending on your choice of Python interpreter, you may or may not have
your system path variable set up correctly. In order to test this, try
starting Wille server in command-prompt by typing::

	wille-admin.py

If the admin script is not found, you need to set up your system path.

* In Windows with Python 2.6 you can add Python Scripts location to PATH by invoking::

	SET PATH=%PATH%;c:\Python26\Scripts
		
* For more information on setting up Python's path variables in Windows, see <http://docs.python.org/using/windows.html#excursus-setting-environment-variables> 
