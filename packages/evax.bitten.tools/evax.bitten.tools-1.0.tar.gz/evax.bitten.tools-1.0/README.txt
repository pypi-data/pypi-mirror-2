evax.bitten.tools
=================

evax.bitten.tools is a Bitten__ plugin adding support for check__ and lcov__

__ http://bitten.edgewall.org
__ http://check.sourceforge.net
__ http://ltp.sourceforge.net/coverage/lcov.php

evax.bitten.tools is provided under a BSD-style license.

Installation
------------

easy_install evax.bitten.tools


Usage
-----

In order to use the plugin in a build configuration, you must define the plugin namespace as follows::

    <build
        (...)
        xmlns:evax="http://www.evax.fr/bitten/tools"
        (...)>

then use it like this::

        <step id="tests" description="Automated tests">
            <c:make file="Makefile" target="check" />
            <evax:check reports="tests/*_check.xml" />
            <evax:lcov directory="src" />
        </step>

Please note that the plugin expects check's xml output format.

