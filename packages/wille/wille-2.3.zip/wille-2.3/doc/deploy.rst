Deploying Wille
===============

Running on a (Linux) Server
---------------------------

While Wille is designed to primarily run on a local machine, it may be deployed
into a server as well. A notable drawback in Wille is that it does not support
any standard server interface such as WSGI, therefore requiring us to manage
the server process by some other means.

One (hacky) option for running Wille on a Linux server is to use `nohup`.
For instance::

	nohup python wille-server.py -p 8080 -v public

Now verify that the process is running::

	ps -ext | grep wille

If everything went fine, you should be able to use the server with a browser
by navigating to:

	http://[yourip]:8080/

For more information on using and configuring Wille Server, see section `Using Wille Server`.

Creating Stand-alone Applications with Wille+Jython
---------------------------------------------------

In order to create a standalone deployment of Wille running on Jython, we
recommend using the following folder structure::

		your-application-root/
			apps/
			services/
			scripts/
			jython/
				...
				Lib/
					site-packages/
						wille/
						httplib2/
						pyjavaproperties/
						feedparser/
						argparse/

You may achieve the structure by proceeding as follows:
* Cope Jython under `jython`
 * Since Jython is quick big (around 40 MB), you may want to exclude some
   parts that are not necessary for simply running Jython.
   These include `Docs`, `Demo` and `tests` folders.
* Copy Wille Python library under `jython/Lib/site-packages/`
 * Note that you also need to copy all depending libraries under site-packages as well
* Adding application specific parts
 * Copy apps, services and scripts under your application root

Now you should be able to run Wille server by invoking::

	java -jar jython/jython.jar wille-server.py
