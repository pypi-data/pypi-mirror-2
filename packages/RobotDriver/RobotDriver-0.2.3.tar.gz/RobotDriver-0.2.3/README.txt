Introduction
============

RobotDriver is a `Trac`_ plugin that adds `RobotFramework`_ support
to `Bitten`_.

.. _`Trac`: http://trac.edgewall.org
.. _`Bitten`: http://bitten.edgewall.org
.. _`RobotFramework`: http://code.google.com/p/robotframework

Installation
============

Installation is done just as for any other Trac plugin. Using the pip or
easy_install command from setuptools is the easiest.

To install using ``pip``::

    pip install robotdriver

To install using ``easy_install``::

    easy_install robotdriver

After that you must configure your Trac project to use the plugin.  Edit
conf/trac.ini in your Trac directory to include this::

    [components]
    robotdriver.* = enabled

If you have downloaded a source tarball you can install it
by doing the following,::

    $ python setup.py build
    # python setup.py install # as root

Example
=======

An example build recipe for Bitten might like this::

    <build xmlns:svn="http://bitten.edgewall.org/tools/svn"
          xmlns:sh="http://bitten.edgewall.org/tools/sh"
          xmlns:robotdriver="http://bitbucket.org/xyb/robotdriver">

        <step id="checkout" description="Checkout source">
          <svn:checkout path="${path}" url="http://svn.douban.com/svn/robotdriver" revision="${revision}"/>
        </step>

        <step id="robot" description="Gather robotframework report">
          <sh:exec executable="pybot" args="-C off -l NONE -r NONE -o output.xml data_sources"/>
          <robotdriver:robot file="output.xml" />
        </step>

    </build>

License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
