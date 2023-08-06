Running Wille on Jython
=======================

Wille mainly works well on Jython. Especially if you wish to create OS
independent, standalone Wille installations, the use of Jython is an appealing
option.

Note however that some Python libraries are not available for Wille; components
requiring these libraries may not work on Jython. Also note that Wille works
notably slower on Jython. For computationally demanding tasks, we do not
recommend using Jython.

Setting up Wille on Jython
--------------------------

When choosing a Jython version, note the following:

* Jython version 2.5.1 or later is required
* Using the latest stable version of Jython is highly recommended

Also note the following differences in Jython:

* Jython's environment variable for module path is JYTHONPATH (not PYTHONPATH)

Known Problems with Jython
--------------------------

Access Violation Exception in Jython
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When running Wille on Jython, the software crashes with an access violation
Exception (EXCEPTION_ACCESS_VIOLATION) from JVM.

This error is known to be caused by using reloader (-r option) when
running Wille Server on Jython.

Workaround: Switch to CPython when you need the reloader

System Crashes when Running Wille on Jython
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Due to unknown reasons, running Wille on the very specific version 2.5.0 of
jython, may crash a system. The problem disappeared and could not be reproduced
on Jython 2.5.1.

Workaround: upgrade Jython to a later version.
