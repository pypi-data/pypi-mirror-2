Wille Services
==============

`Wille Services` are the building blocks of data processing pipelines used in
creation of visualisations. Wille services can be executed either locally or
from a remove source (over HTTP).

Services are located under your project folder in `services` directory::

	services/
		myservice/
			willeservice.properties
			
A service description file (willeservice.properties) is required. Note that
all the files used by the service should be located under the service folder.
Resources shared between several services have to be located under `libs`
folder.

Creating a Service
------------------

Make sure you are at your services folder::

	cd my-project/services

The easiest way to start creating a new Wille service is to use `wille-admin`
script::

	wille-admin.py createservice myservice
	
A new folder containing all the required files for your service will be
created.

Writing Service Adapter
-----------------------

Components used in creation of Wille services, may be written in a host of
languages. The key to adapting components as new services to Wille is
`willeservice.properties` file. Properties file contains all necessary
information to wrap a component as a service to Wille. Services properties is
a plain Java property file, containing key-value -pairs. The following
properties are recognised by Wille.

type
^^^^

Used to specify type of the service. Services sharing a type can be used
interchangeably. For instance, two XSL processors can be written to share
type `xslt` and when a script is executed, it may freely choose which one
of the processors it will use.

description
^^^^^^^^^^^

Description of the service

adapter
^^^^^^^

Specifies which adapter is used to wrap a component. By default, the following
adapters are available:

**PythonService**

Loads service definition from Python file. Set adapter.command to point to the
class that implements the service.

**CommandLine**

Command-line adapter to wrap any local, command-line command as a service
								
When using "CommandLine" adapter, you must make sure yourself that nothing is
overwritten, e.g. when service is executed in parallel by several callers.
								
Any non-zero return values from command-line command are considered as errors
and will result in adapter execution error
(can be ignored by adding property `adapter.errors=ignore`)								
								
Command-line services do not use any kind of automated security model
or sandboxing and hence, you should be very considered about what is allowed to
run as a command-line service!
								
**IsolatedCommandLine**

Same as command-line, but isolates each execution by copying all files from
service directory into isolated, per-instance, temporary folder.
								
Isolated command-line is not as efficient as CommandLine adapter since it
copies all the files under the service directory into a temporary location
PER SERVICE EXECUTION.
								
Remember that isolated command-line can not depend on any other services
relative to its location since it will be ran as an ISOLATED service.
																						         
It is generally a bad idea to add read-only files under service
directory when using isolated command-line adapter: they do not get
deleted under Windows (due to an issue with Python's `shutil.rmdir` function) 							         							

**HTTPGet**

Retrieves content with HTTP/GET from URL specified in ^adapter.comman^. Other
adapter properties are ignored.

adapter.command
^^^^^^^^^^^^^^^
																          
Command that is passed to adapter for execution. Writing adapter command is the
key to successfully wrapping components as service.
												
Example command for a ^CommandLine^ adapter::

	software.exe --inputfile=@{inputfile} --param1=${param1}
																						
When inputfile and param1 are given as parameters:

* `@{param}` is replaced with a file in which data from parameter is saved
* `${param}` is replaced with parameter's value

Note that some Wille-specific parameters are always available as follows:						

* `${_libs}` - Absolute path to Wille Libs

adapter.output
^^^^^^^^^^^^^^

Specifies the filename to which output for the service is written.
Only used together with `CommandLine` and `IsolatedCommandLine` adapters.

The property is interpreter as follows:

* value empty or missing: returns console output (`stdout`) as a result
* single filename: returns content of a file
* directory name with a filename: returns multiple files in a ZIP package

adapter.output.type
^^^^^^^^^^^^^^^^^^^ 
						
Force a specific output type as result. Valid values:

* `stdout` - capture result from standard console output
* `file` - return file as a result
* `directory` - return directory in a ZIP

adapter.output.format
^^^^^^^^^^^^^^^^^^^^^							

Force a specific output format.
							
Specify format as result's MIME type (see <http://www.iana.org/assignments/media-types/>).
							
Some typical MIME types:
* application/json (JSON)
* application/xml (XML)
* application/zip (ZIP)
* image/jpeg (JPEG)
* image/svg+xml (SVG)

adapter.output.encoding
^^^^^^^^^^^^^^^^^^^^^^^

Force a specific output encoding. Default is UTF-8
							
parameters
^^^^^^^^^^

A comma-separated (,) list of parameters
	
By default, all parameters are required. Parameter can be specified as
optional, by wrapping it with parenthesis ()
						
Typing can be added to parameters with properties `parameters.[name].type`.
The following types are supported:

* `password` - password field
* `date` - date field (YYYY-MM-DD)
* `time` - time field (HH:MM:SS)
* `datetime` - date & time field (YYYY-MM-DD HH:MM:SS)

profile
^^^^^^^				

A comma-separated (,) list of profiles the service belongs to.
    				    			
By default, a service does not a have specific profile.If profiles are
specified, the service will be enabled only when at least one of the
specific profiles has been loaded.    					
					 