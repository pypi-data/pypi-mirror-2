=============
munin.varnish
=============

Introduction
============

A buildout recipe that packages and configures the munin tool
*varnish_* to enable monitoring of Varnish.

Contains a modified version of *varnish_*
`r4439 <http://varnish-cache.org/browser/trunk/varnish-tools/munin/varnish_?rev=4439>`__
created by Kristian Lyngstol which works with Varnish 2.0 or newer.


How to use it
=============

You can use it with a part like this::

    [buildout]
    parts =
      ...
      munin-varnish

    [munin-varnish]
    recipe = munin-varnish
    varnishstat = ${varnish-build:location}/bin/varnishstat

Where ``varnish-build`` would be a typical cmmi part that builds
Varnish. And the ``varnishstat`` option is the full path to the
*varnishstat* binary.


This part will create a script in the buildout bin directory called
*munin-varnish* which is used to monitor all the different aspects. The
current list of aspects available for monitoring is (``bin/munin-varnish suggest``)::

    expunge
    transfer_rates
    objects
    uptime
    request_rate
    memory_usage
    hit_rate
    threads
    backend_traffic

Each of these need to be installed as symlinks into the munin-node
plugins. For example::

    cd /etc/munin/plugins
    ln -s /path/to/buildout/bin/munin-varnish varnish_expunge


Monitoring multiple instances
-----------------------------

You can use the optional parameter `name` to add a name to the
graph titles::

    [munin-varnish]
    recipe = munin-varnish
    varnishstat = ${varnish-build:location}/bin/varnishstat
    name = Project X


In the above Example calling ``graph_title Object expunging`` would become
``graph_title Object expunging - Project X``.

To monitor multiple instances you need to be able to put different symlinks
into your ``etc/munin/plugins/`` directory.
You can use double underscore in the symlink installation to separate the
instance name from the aspect.
The above installation example would become::

    cd /etc/munin/plugins
    ln -s /path/to/buildout/bin/munin-varnish varnish_projectX__expunge

(**ATTENTION**: note the double underscore!).

We are using a slightly modified version of *varnish_* to support multiple instances.
See this `post on varnish-dev <http://lists.varnish-cache.org/pipermail/varnish-dev/2009-December/002347.html>`__
for more information.

Notes
=====

* A build of *varnishstat* requires the developer's libraries for
  ncurses. If you don't have a *varnishstat* in your build of Varnish
  then most likely you need to install the ncurses-devel or
  libncurses5-dev package and then get buildout to rebuild Varnish.

* The hit_rate aspect only works correctly with a munin server running
  version 1.4.0 alpha or better. However hit rate data is also
  available in request_rate where it is presented as raw rates rather
  than normalized as a percentage.

Credits
=======

Michael Dunstan, Author

Harald Friessnegger, added support for multiple instances


