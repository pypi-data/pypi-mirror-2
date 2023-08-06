Wille Server
============

Running Server
--------------

In order to run Wille Server from a command-line, first change your working
directory into one of your Wille projects::

	cd myproject

If your command-line path is set up correctly, you can now start Wille Server
by invoking::	

	wille-admin.py runserver
	
Alternative, you can use a shorthand script for running the server::

	wille-server.py

To confirm that server is running, enter http://localhost/ with your web browser

You can now stop the server by pressing `CTRL+C`.

Configuring Server
------------------

Wille Server can be configured, by using commmand-line parameters. in order to
see a full list of available parameters, use `-h` option::

	wille-server.py -h

Port
^^^^

By default, Wille runs on port `80`. However since this port is reserved for
HTTP, you may need to customise the port in which your Wille server is running.
In order to do so, use `-p` parameter::

	wille-server.py -p 8080

Access Control
^^^^^^^^^^^^^^

Note that by default, for security reasons, Wille services and apps are visible
to localhost only by. Other visibilities can be configured from command-line by
setting --visibility parameter:

In order to share your server to specific IP addresses, provide them in a
comma-separated string::

	wille-server.py -v 192.168.0.1,192.168.0.2
	
In order to disable access control, set value to `public`::

	wille-server.py -v public

Important security note: Wille server automatically shares all hosted apps and
services with same access rights. Hence, sharing even a single app/service to
a specific location means all other running components are also visible.

	