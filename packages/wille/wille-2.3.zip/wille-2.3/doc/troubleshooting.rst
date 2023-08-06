Troubleshooting
===============

Debugging with Wille Server
---------------------------

Best way to troubleshoot Wille Server is to run it with debug mode enabled
by invoking::

	wille-server.py -d

Debug mode will enable more verbose output from Wille server to the command-line
console. It also enables you to more often and easily capture stack traces and
error messages not from Python only, but from Wille services as well.

Migrating from Earlier Versions
-------------------------------

Migrating from Wille 2.2
^^^^^^^^^^^^^^^^^^^^^^^^

* As of Wille 2.3 userdata folder is located by default under your project folder (`myproject/data`)
 * In Wille 2.2, userdata folder was per-user. If you still desire to use per-user data folders,
   this setting can be configured with Wille server's `-u` option   
* `wille.views.contrib` and `wille.views.core` has been renamed to `wille.views`
 * Scripts using `core` or `contrib` modules need to be changed to import `wille.views` instead

Common Problems
---------------

socket.error [Errno 13]: Access denied
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Socket error typically means that Wille has not enough priviledges to open
a new socket listener for a specific port.

In Linux running Wille on ports below 1024 requires administrative rights.
This can be managed by parametrising Wille server to use an accessable port,
such as port number 8080 as follows: python wille-server.py -p 8080
	      
If you really need to run Wille on a specific port, such as 80, you
need to run Wille via sudo (sudo python wille-server.py). Due to
potential security risks, however, this is not recommended option.

ImportError: No module named wille.XXX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure that Wille has been installed into a location included in your
PYTHONPATH. For more information on installing and configuring Wille, see
section `Installation`.

Wille Server Returns Blank HTTP responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Responses from any Wille Server page are blank and return code
"HTTP/1.x 404 Not Found". This inconvenient error occurs sporadiously.
It is suspected that the error has something to do with Wille Server's bootup
sequence (everything is not loaded in correct order every time).

Workaround: Restart Wille Server.

Overlapping Module Names
^^^^^^^^^^^^^^^^^^^^^^^^
Dynamically loaded Python apps and services that have same module name
(e.g. service1/run.py and service2/run.py) overlap: the last one overwrite
the earlier ones.

Workaround: Rename modules uniquely.

Error code 401 (Unauthorized) When accessing Wille Server via a Proxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is known that accessing Wille via a web proxy may lead to HTTP response with 
error code 401 (Authorized). Formally, Wille does not support web proxy servers
so this behaviour may be well expected.

If you really need to access Wille services with a proxy, as a workaround,
you may add the IP address/addresses of you proxy server to Wille's visibility
list when starting the server. Note that after this, other users of the same
proxy servers may be able to access your server as well.It is known that
accessing Wille via a web proxy may lead to HTTP response with error code
401 (Authorized). Formally, Wille does not support web proxy servers so this
behaviour may be well expected.

Workaround: If you really need to access Wille services with a proxy, you may
add the IP address/addresses of you proxy server to Wille's visibility list
when starting the server. Note that after this, other users of the same proxy
servers may be able to access your server as well.
