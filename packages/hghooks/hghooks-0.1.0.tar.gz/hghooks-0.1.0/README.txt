.. contents::

=======
hghooks
=======

hghooks is a simple module that adds several useful hooks for use in
Mercurial hooks system.

Right now it includes hooks for:

 * pep8 checking of python files
 * pyflakes checking of python files
 * checking for forgotten pdb statements in python files


Documentation
=============

Installation
------------

hghooks is distributed as a Python egg so is quite easy to install. You just
need to type the following command::

 easy_install hghooks

And Easy Install will go to the Cheeseshop and grab the last hghooks for you.
It will also install it for you at no extra cost :-)


Usage
-----

To use one of the hooks provided by this package edit your hgrc file of
your Mercurial repository and add these lines::

 [hooks]
 pretxncommit.pep8 = python:hghooks.pep8hook.pretxncommit
 pretxncommit.pyflakes = python:hghooks.pyflakeshook.pretxncommit
 pretxncommit.pdb = python:hghooks.pdbhook.pretxncommit

You can add only the hooks that you need.
