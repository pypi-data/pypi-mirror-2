RobotDriver is a Trac__ plugin that adds RobotFramework__ support
to Bitten__.

__ http://trac.edgewall.org
__ http://code.google.com/p/robotframework
__ http://bitten.edgewall.org

Example:

An example build recipe might like this:

<build xmlns:svn="http://bitten.cmlenz.net/tools/svn"
      xmlns:sh="http://bitten.cmlenz.net/tools/sh"
      xmlns:robotdriver="http://bitbucket.org/xyb/robotdriver">

    <step id="checkout" description="Checkout source">
      <svn:checkout path="${path}" url="http://svn.douban.com/svn/robotdriver" revision="${revision}"/>
    </step>

    <step id="robot" description="Gather robotframework report">
      <sh:exec executable="pybot" args="-l NONE -r NONE -o output.xml data_sources"/>
      <robotdriver:robot file="output.xml" />
    </step>

</build>

Installation:

Installation is done just as for any other Trac plugin.  Using the
easy_install command from setuptools is the easiest (provided you have
already setuptools installed):

easy_install robotdriver

After that you must configure your Trac project to use the plugin.  Edit
conf/trac.ini in your Trac directory to include this:

[components]
robotdriver.* = enabled
