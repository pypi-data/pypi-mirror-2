py.test plugin for checking PEP8 source code compliance using the pep8 module.

Usage
---------

install via::

    easy_install pytest-pep8 # or
    pip install pytest-pep8

and then type::

    py.test --pep8
    
to activate source code checking. Every file ending in ``.py`` will be
discovered and checked, starting from the command line arguments::

    py.test --pep8 mysourcedir # or
    py.test --pep8 mysourcedir/somefile.py

Running PEP8 checks and no other tests
---------------------------------------------

You can also restrict your tests to only run "pep8" tests and not
your other tests by typing::

    py.test --pep8 -k pep8

This will only run tests that are marked with the "pep8" keyword
which is added for the pep8 test items added by this plugin.

Looking at currently active PEP8 options
---------------------------------------------

Note that in the testing header you will see the current list of default "ignores"::

    pep8 ignore opts: E202 E221 E222 E241 E301 E302 E401 E501 E701 W293 W391 W601 W602

For the meaning of these error and warning codes, see the error output
when running against your files or checkout `pep8.py
<https://github.com/jcrocholl/pep8/blob/master/pep8.py>`_.

Configuring PEP8 options per-project
---------------------------------------------

Lastly, you may configure PEP8-checking options for your project
by adding an ``pep8options`` entry to your ``pytest.ini``
or ``setup.cfg`` file like this::

    [pytest]
    pep8options = +W293 -E200


Notes
-------------

The repository of this plugin is at http://bitbucket.org/hpk42/pytest-pep8

For more info on py.test see http://pytest.org

The code is partially based on Ronny Pfannschmidt's pytest-codecheckers plugin.

