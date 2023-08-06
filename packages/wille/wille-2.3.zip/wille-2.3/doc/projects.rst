Wille Projects
==============

Wille projects are configurations of different Wille components. A Wille
project is simply a folder in which different components are organised by
a convention.

By default, Wille projects are organised according to the following structure::

	myproject/
		services/
			service1/
			service2/
		apps/
			app1/
			app2/
		scripts/
		libs/
			
* `Wille Services` are located under `services` folder (one folder per service).
* Similarly `Wille Apps` are located under `apps`folder.
* `Scripts` which are part of the project and may use Wille, but are not either services or apps, should be placed under `scripts` folder.
* `Libs` folder contain different libraries that maybe shared among various components.

Creating a Project
------------------

Easiest way to create a new Wille project is to use `wille-admin` script. For
instance, we can create new project named `myproject` by invoking::

	wille-admin.py createproject myproject

A new project with subdirectories according to convention are created.
