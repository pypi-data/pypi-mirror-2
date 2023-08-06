# Documentation Uploader 0.10 README

## Introduction
DocUp: Automatically get your Markup text files on to PyPI

DocUp uses Markup to convert text files in Markup format to HTML,
put them into a zip folder, and upload the whole thing to PyPI

## Prerequisites

* Python 2.4.3 or newer
* Markdown 1.0.1
* Zip 2.31

Download and compile Python 2.4.3:

    $ VERSION=2.4.3
    $ mkdir /tmp/src 
    $ cd /tmp/src/
    $ wget http://python.org/ftp/python/$VERSION/Python-$VERSION.tar.bz2
    $ tar xjf Python-$VERSION.tar.bz2
    $ rm Python-$VERSION.tar.bz2
    $ cd Python-$VERSION 
    $ ./configure
    $ make
    $ sudo make altinstall

Now we need to install Python setuputils:

    $ cd /tmp/src
    $ wget http://pypi.python.org/packages/2.4.3/s/setuptools/setuptools-0.6c11-py2.4.3.egg
    $ sudo sh setuptools-0.6c11-py2.7.egg

Now install pip to install the rest of our dependencies:

    $ sudo easy_install pip

Now we install Markdown:

    $ sudo pip install markdown

Zip should be pre-installed, but to install it on Redhat-derived distros, use:

    $ sudo yum install zip

or, on Debian-based distros:

    $ sudo apt-get install zip

on Debian-derived distros.

And now for DocUp itself:
 
    $ sudo pip install DocUp


##Syntax

In order to upload a file, directory, or comma-seperated list of files to PyPI as documentation,
follow this pattern:

    $ ./DocUp.py <file1[,file2,...]> <project-name> [username:password]

or

    $ ./DocUp.py <directory> <project-name> [username:password]


*	file1[,file2...] - file1 refers to a single text file that could be uploaded for documentation. Optionally, comma-seperate any more files you would like to add.

*	project-name - The project to which the documentation will be uploaded.

*	username:password - The username and password of the PyPI user under whom you want to post the documentation. (Only required when .pypirc is not present or configured properly.)

*	directory - A directory to be uploaded as documentation.

NOTE: If you want a file converted from markdown to html, make sure it has a .txt extension.

## License

See LICENSE for details.



