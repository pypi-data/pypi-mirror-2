Why?!
=====

Daily programming tasks, such as code compilation and running automated tests, often consumes a lot of time even on rather small projects.

While alt-tabbing away from the command you just started, this simple tool will help you to get back on your development track as soon as possible.

Saving you minutes every day :)


Installation
============

On Linux with pip::

    sudo pip install naf

On Linux from source::

    git clone git://github.com/knutz3n/naf.git
    cd naf
    sudo python setup.py install

On Mac OS X (with Growl installed)::

    sudo easy_install growl-py
    sudo easy_install naf

On Windows:
In theory, ``naf`` should work on Windows wth Growl for Windows (http://www.growlforwindows.com/) and growl-py installed.
I would highly appreciate any feedback on this.


Usage
=====

::

    naf mvn clean install

This will run ``mvn clean install`` and notify you when the command has exited with the exit code it returned.
