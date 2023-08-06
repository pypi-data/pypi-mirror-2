Pyg's config files
==================

.. versionadded:: 0.4

Config files allow you to override command-line options, and to save them somewhere.
During the initialization process, Pyg looks for configurations file, it this order:

    * :file:`./pyg.conf`: a configuration file in the current working directory:
    * :file:`~/pyg.conf`: where ``~`` stands for your :envvar:`HOME` directory;
    * :file:`~/.pyg/pyg.conf`.

A config file has this structure::

    [section_name]
    option = value

    [section_name2]
    option1 = value1
    option2 = value2
    
    ...


In addition to this, Pyg supports a nonstandard syntax, allowing multiple section names in a single header::

    [section1 & section2 & section6]
    option = value

And it will set that option in all specified sections.

Example usage
-------------

Example 1
+++++++++

:file:`~/pyg.conf`::

    [remove]
    yes = True
    
    [install]
    upgrade_all = True

Pyg::

    $ pyg install iterutils
    Loading options from ~/pyg.conf
    iterutils is already installed, upgrading...
    Looking for iterutils releases on PyPI
    Best match: iterutils==0.1.6
    Downloading iterutils [100% - 2.9 Kb] 
    Checking md5 sum
    Running setup.py egg_info for iterutils
    Running setup.py install for iterutils
    iterutils installed successfully
    $ pyg remove iterutils
    Loading options from ~/pyg.conf
    Uninstalling iterutils
            /usr/local/lib/python2.7/dist-packages/iterutils.py
            /usr/local/lib/python2.7/dist-packages/iterutils.pyc
            /usr/local/lib/python2.7/dist-packages/iterutils-0.1.6-py2.7.egg-info
    Deleting: /usr/local/lib/python2.7/dist-packages/iterutils.py
    Deleting: /usr/local/lib/python2.7/dist-packages/iterutils.pyc
    Deleting: /usr/local/lib/python2.7/dist-packages/iterutils-0.1.6-py2.7.egg-info
    Removing egg path from easy_install.pth...
    iterutils uninstalled succesfully

Example 2
+++++++++

:file:`~/pyg.conf`::

    [freeze]
    count = True

Pyg::

    $ pyg freeze
    Loading options from ~/pyg.conf
    84

Example 3
+++++++++

You can also override saved options from the command line.
:file:`pyg.conf`::

    [install]
    index_url = http://pypi.python.org/pypi

Pyg::

    $ pyg install itertools_recipes -U --index-url = http://pypi.python.org/simple
    itertools_recipes is already installed, upgrading...
    Looking for links on http://pypi.python.org/simple
            Found: itertools_recipes-0.1.tar.gz
            Downloading itertools_recipes [100% - 2.3 Kb] 
            Running setup.py egg_info for itertools_recipes
            Running setup.py install for itertools_recipes
    itertools_recipes installed successfully

instead of::

    $ pyg install -U itertools_recipes
    itertools_recipes is already installed, upgrading...
    Looking for itertools_recipes releases on PyPI
    Best match: itertools_recipes==0.1
    Downloading itertools_recipes [100% - 2.3 Kb] 
    Checking md5 sum
    Running setup.py egg_info for itertools_recipes
    Running setup.py install for itertools_recipes
    itertools_recipes installed successfully

Option tree
-----------

Here is a list of all sections and their default options:

    **install**:

        - *upgrade* = False
        - *upgrade_all* = False
        - *no_deps* = False
        - *index_url* = ``http://pypi.python.org/pypi``
        - *install_dir* = :data:`pyg.locations.INSTALL_DIR`
        - *user* = False
        - *no_scripts* = False
        - *ignore* = False

    **remove**:

        - *yes* = False

    **bundle**:

        - *exclude* = None

    **update**:

        - *yes* = False

    **download**:

        - *unpack* = False
        - *download_dir* = :file:`.`
        - *prefer* = None

    **freeze**:

        - *count* = False
        - *file* = None

    **unlink**:

        - *all* = False