Radish
====================================

Radish is a set of common tools for testing django projects 
with lettuce.  The goal of this project is to capture the
most common test utilities in one place to reduce the time
it takes to set up BDD on a new project.


Radish Settings
====================================

The default browser used by Radish is 'firefox'.

You will also need to define LETTUCE_APPS to include radish:

    LETTUCE_APPS = ('radish',...)

Don't forget to include other apps that you are testing with
lettuce and that rely on radish.

To log in as a superuser into the django admin you'll want to
create a superuser account and put those credentials in the
settings_test.py file.  Radish will use these to log in, or
default to the username/password of admin/admin:

    RADISH_ADMIN_LOGIN = 'admin'
    RADISH_ADMIN_PASSWORD = 'admin'

Please be warned, shipping your code with this superuser is 
highly discouraged.


Terrain.py
====================================

Testing with lettuce requires that you set up a terrain.py
file in the root of your django project or in each features/
folder.  Radish comes with a predefined terrain file called
dirt.py.  You can define your own terrain.py file or use 
dirt.py by importing it:

    from radish.dirt import *

That should set up your testing environment nicely.


How to test the application
====================================

It's recommended that you set up a different settings file
called settings_test.py for use with Radish.  This will 
prevent you from entering test data into your database by
accident.

    python manage.py syncdb --settings=settings_test

Creates the test DB (with the same basic data of syncdb)

    python manage.py harvest --settings=settings_test -d

Launches the lettuce test suite against the test DB.
The "-d" option launches Django in the development mode.
To test only one application use -a, e.g.: "-a pictures"
To test only one scenario us -s, e.g.: "-a pictures -s 1"

How to test the application without GUI
====================================

Lettuce uses selenium to launch tests inside the browser. 
If the browser cannot be launched with a proper GUI 
(e.g., on a remote server), then the tests can
still be run, but the following steps are required:

    aptitude install xorg xserver-org xvfb xinit x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
    startx -- `which Xvfb` :99 -screen 0 1024x768x24
    env DISPLAY=:99

These steps set up a virtual display called ":99" (can be changed to whatever
string). Firefox automatically reads this environment variable and executes the
tests with that output.

If the tests are run through a virtual machine, Firefox can be still spawned on the local machine by adding the -X option to the ssh command, e.g.:
    ssh virtual_machine -X

In case of error in a test, the last Firefox screenshot can always be accessed
at tmp/last\_failed\_scenario.png
