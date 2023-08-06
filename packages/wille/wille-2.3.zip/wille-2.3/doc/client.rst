Wille Client
============

`Wille Client` is the part of the framework that can be used to create
visualisation and data processing pipelines with Wille. With Wille Client
you can specifically:

    * Find and execute Wille services,
    * Manage user data and credentials, and
    * Launch visualisations (in stand-alone mode) 

Wille Client can be used either in stand-alone mode (Python scripts) or as
part of other Wille Services and Apps.

Service Discovery and Execution
-------------------------------

Let us consider that we want to use Wille Client in an arbitrary Python script
for discovering and executing a PDF2TXT converter service.

First, import Wille Client module and create an instance::

	import wille.client
	client = wille.client.Client(debug=False)

Load services to the client and for verification, display a list of them::

	client.load_dir('../../services')
	print "Services loaded: ", client.services()

Execute a PDF2TXT converter service with an example PDF file::

	data = open('data/example.pdf').read()
	result = client.execute_service(type='pdf2txt', params={'filename.pdf': data})

Examine if the execution was successful and display results / error::

	if result.metadata['success']: 
   		print (result.data)
	else:
   		print ("ERROR:\n", result.data)

Working with User Data
----------------------

Wille client supports use of an external user data folder for persistent
storage of user data.

By using user data folder, the previous result could be saved under userdata
folder as follows::

	import os
	filename = os.path.join(client.userdata_dir, 'result.txt')
	file = open(filename, 'w')
	file.write(result.data)
	file.close()
	print ("Wrote %s" % filename)
	
By default, userdata folder is located under `data` folder in your Wille
project. data. During instantiation of Wille client, you may choose to use
another userdata folder instead, with userdata_dir argument.

Using Keyring
^^^^^^^^^^^^^

Wille client carries a keyring that can be used to manage user various tokens
for authenticating user to various resources and services. Two types of tokens
are currently supported: username and API key tokens, but new token types may
be introduces as necessary.

Tokens can be added to the keyring as follows:

Adding a password token::

	client.keyring.add_token_username('email', 'password', domain='example.com')
	 
Adding an API key token::

	client.keyring.add_token_apikey('apikey', 'secret', domain='api.example.com') 

Optional domain argument allows you to specify a domain (or domains) for
which the token is valid.

Keys from keyring can be obtained as follows:

Return all keys from keyring::

	client.keyring.keys()
	 
Return all API keys valid for domain api.flickr.com::

	client.keyring.keys(type='APIKeyToken', domain='api.flickr.com') 

Once new keys have been added, you may want to save your keyring for later use::

	client.save_keyring()
