restarter
=========

`restarter` is a little utility to restart services if referenced objects
like executables or shared libraries have changed on disk. The aim is to ensure
that all services run current versions of their software. This is important for
example after security updates.


Usage
-----

`restarter` takes a pidfile as required argument. If the service is stale, that
means there are replaced objects still held in memory, `restarter` executes the
restart command passed via the `--restart` option::

   restarter --restart "/etc/init.d/atd restart" /var/run/atd.pid

There is also the possibility to speficy a "hard restart" command that is
executed if the regular restart command fails.

See the output of `restarter --help` for a list of all supported options.


Stopped Services
----------------

Stopped services are gracefully ignored: `restarter` does nothing if the pidfile
does not exist or the pid referenced therein is not running. This behaviour can
be modified with the `--fail` option. Note that `restarter` always fails when
the service was running but did not come up again after restart.


.. vim: set ft=rst:
