template: doc.html
title: News

_TOC_TOP_

.. contents::
    :backlinks: top

_TOC_BOT_

0.10.0 / 2010-07-08
-------------------

- New HTTP parser.
- New HUP behaviour : 
  - Reload configuration
  - Start the new worker processes with a new configuration
  - Gracefully shutdown the old worker processes
- New gevent worker "egg:gunicorn#gevent2", working with gevent.wsgi.
- New documentation site.
- Refactoring of configuration
- Fixed QUIT with eventlet worker
- Added an example reloader config
- Allows people to pass info from the command line to a WSGI application. See `examples/alt_spec.py <http://github.com/benoitc/gunicorn/raw/master/examples/alt_spec.py>`_ example::

  $ gunicorn 'alt_spec:load("my arg here")'

0.9.1 / 2010-05-26
------------------

- Support https via X-Forwarded-Protocol or X-Forwarded-Ssl headers
- Fix configuration
- Remove -d options which was used instead of -D for daemon.
- Fix umask in unix socket

0.9.0 / 2010-05-24
------------------

- Added *when_ready* hook. Called just after the server is started 
- Added *preload* setting. Load application code before the worker processes
  are forked.
- Refactored Config
- Fix pidfile
- Fix QUIT/HUP in async workers
- Fix reexec
- Documentation improvements

0.8.1 / 2010-04-29
------------------

- Fix builtins import in config
- Fix installation with pip
- Fix Tornado WSGI support
- Delay application loading until after processing all configuration

0.8.0 / 2010-04-22
------------------

- Refactored Worker management for better async support. Now use the -k option
  to set the type of request processing to use
- Added support for Tornado_


0.7.2 / 2010-04-15
------------------

- Added --spew option to help debugging (installs a system trace hook)
- Some fixes in async arbiters
- Fix a bug in start_response on error

0.7.1 / 2010-04-01
------------------

- Fix bug when responses have no body.

0.7.0 / 2010-03-26
------------------

- Added support for Eventlet_ and Gevent_ based workers.
- Added Websockets_ support
- Fix Chunked Encoding
- Fix SIGWINCH on OpenBSD_
- Fix `PEP 333`_ compliance for the write callable.

0.6.5 / 2010-03-11
------------------

- Fix pidfile handling
- Fix Exception Error

0.6.4 / 2010-03-08
------------------

- Use cStringIO for performance when possible.
- Fix worker freeze when a remote connection closes unexpectedly.

0.6.3 / 2010-03-07
------------------

* Make HTTP parsing faster.
* Various bug fixes

0.6.2 / 2010-03-01
------------------

* Added support for chunked response.
* Added proc_name option to the config file.
* Improved the HTTP parser. It now uses buffers instead of strings to store
  temporary data.
* Improved performance when sending responses.
* Workers are now murdered by age (the oldest is killed first).


0.6.1 / 2010-02-24
------------------

* Added gunicorn config file support for Django admin command
* Fix gunicorn config file. -c was broken.
* Removed TTIN/TTOU from workers which blocked other signals.

0.6 / 2010-02-22
------------------

* Added setproctitle support
* Change privilege switch behavior. We now work like NGINX, master keeps the
  permissions, new uid/gid permissions are only set for workers.

0.5.1 / 2010-02-22
------------------

* Fix umask
* Added Debian packaging

0.5 / 2010-02-20 
----------------

* Added `configuration file <configuration.html>`_ handler.
* Added support for pre/post fork hooks
* Added support for before_exec hook
* Added support for unix sockets
* Added launch of workers processes under different user/group
* Added umask option
* Added SCRIPT_NAME support
* Better support of some exotic settings for Django projects
* Better support of Paste-compatible applications
* Some refactoring to make the code easier to hack
* Allow multiple keys in request and response headers

.. _Tornado: http://www.tornadoweb.org/
.. _`PEP 333`: http://www.python.org/dev/peps/pep-0333/
.. _Eventlet: http://eventlet.net
.. _Gevent: http://gevent.org
.. _OpenBSD: http://openbsd.org
.. _Websockets: http://dev.w3.org/html5/websockets/
