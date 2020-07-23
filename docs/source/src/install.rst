Installation Guide
==================

To install ``gdutils`` package, run the following ``pip`` command:
::

    $ pip install git+https://github.com/KeiferC/gdutils.git


Manual Installation
-------------------

To manually install ``gdutils`` package, clone the repository with the
following command:
::

    $ git clone https://github.com/KeiferC/gdutils.git

To install the dependecies and a local ``gdutils`` build, run the
following commands:
::
    
    $ cd gdutils
    $ pip install --upgrade pip
    $ python setup.py bdist_wheel
    $ pip install dist/*.whl

Alternatively, if you have a \*nix OS, you can install dependencies and
a local build using ``make``. 

If you only wish to use the ``gdutils`` module in a specific project directory,
clone the ``gdutils`` repository into your project directory and install 
dependencies running ``pip install -r requirements.txt`` inside the cloned
directory.
