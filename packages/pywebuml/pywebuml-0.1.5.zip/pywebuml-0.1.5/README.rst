This package will parse c#, java or python files, and generate the
UML class diagram using a web interface. 

It has 2 commands::

    >>> pywebuml initialize

This command it is used to parse the files. This will create the database and
parse all the files.::

    >>> pywebuml web

This command will start the web interface that will be used to see the class
diagrams.

It is required that `graphviz`_ is installed (and added to the PATH in Windows).

.. _`graphviz`: http://www.graphviz.org

Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_
- `Flask`_


.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
.. _`Flask`: http://pypi.python.org/pypi/Flask
