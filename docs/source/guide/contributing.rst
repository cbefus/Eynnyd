.. _contributing:

Contributing
============

Bugs and Features
-----------------

If you have ideas for new features or bug fixes that you would like done in Eynnyd please feel free to open an issue
in our `Github issue page <https://github.com/cbefus/Eynnyd/issues>`__.


Open for Contributions
----------------------

Eynnyd is a project of passion, not one to make money, so we welcome any help we can get.  If you want to
contribute, feel free to fork our repo, and clone the fork to your machine.  From there you will want to
be able to run the test suite.

.. code:: bash:

    pip install -r test_requirements.txt

Will install everything you need to run the tests.

.. code:: bash:

    python -m unittest discover tests

Will run all of the tests.

You will also want to make sure you maintain 100% test coverage for anything you add. Once you have
installed the test requirements (as above) you can run a coverage report via:

.. code:: bash:

    coverage run --source src/ -m unittest discover tests/
    coverage report


Generating Documentation
------------------------

If you want to build a local copy of these documents to your own machine you can run:

.. code:: bash:

    pip install -r documents_requirements.txt
    cd docs/
    make html

This will generate a file at :code:`docs/build/html/index.html` that can be opened using your browser.




