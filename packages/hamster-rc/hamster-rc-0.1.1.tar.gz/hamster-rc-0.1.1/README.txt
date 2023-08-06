.. contents::

Hamster RC
==========

Hamster RC (Remote Control) is a little web application that lets you control
the Hamster time tracker running on your desktop from a remote browser as the
one running on your mobile device.

So far it shows the facts made the current day and lets you start and stop a
new activity. It communicates with Hamster via DBus.

I wrote it because many times I have to go here and there in the office and
I don't spend the whole day sitting at my desk. I need to track where I spent
my time and carrying my phone around is something I usually do anyway. I have
my desktop IP address saved as a bookmark in my mobile browser so it's quite
easy to access Hamster now :-)

Installation
------------

Just type::

  easy_install hamster-rc

Remember that you need python binding for dbus installed. Unfortunately this
is it not easy in an isolated environment such as virtualenv or buildout.
In my preferred distribution (Fedora) this is provided by the dbus-python
package. The rest of python dependencies (mako, webob and routes) are installed
automatically by easy_install.

Usage
-----

Once it is installed, run it like this::

  hamster-rc --host=192.168.0.2 --port=10000

and it will listen on that IP address and TCP port. It runs on localhost:8888 by
default, which is not very useful since you want to access it from the outside.

Now, point your browser to http://192.168.0.2:10000 and just click on the buttons!

Development
-----------

You can get the last bleeding edge version of hamster-rc by getting a clone of
the Mercurial repository::

  hg clone https://bitbucket.org/lgs/hamster-rc

Future
------

Some features I may implement in the future are:

 - Simple authentication
 - HTML5 local storage support for saving the facts when you lost connection to
   the server. Later, when there is connection again, it could sync these facts
   back to Hamster.

Feel free to send me patches for these and other features you would like to
have. Other feedback is also welcomed.
