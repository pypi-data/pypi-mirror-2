Manual
++++++

TornadoPack provides two things:

* a slightly modified version of the Tornado ``HTTPServer`` where the host can
  be set

* a CommandTool command for running a Tornado server using the infrastructure
  provided by ServiceProvider

It is used something like this:

.. include :: ../../example/run.py
   :literal:

If you save the above file as ``run.py`` you'll be able to serve the
application with:

::

    python run.py app.conf serve

The server and port are set in the config file, ``app.conf`` which looks like this:

.. include :: ../../example/app.conf
   :literal:

When you make changes to and Python modules the server is using, it will
automatically restart.

If you start the server and visit http://127.0.0.1:8000 you'll see the message
"Hello, world!".

The ``ServeCmd()`` class takes one argument which is a list of service to run
on each request. In this case we just run the ``hello`` service.
