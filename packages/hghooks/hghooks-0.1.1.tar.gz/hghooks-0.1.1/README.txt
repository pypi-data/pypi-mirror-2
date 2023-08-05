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

How to skip the hooks
---------------------

If you need to avoid a hook for a specific changeset you can add one or
more of the following keywords to the commit message: no-pep8,
no-pyflakes and no-pdb.

On the other hand, if you want to avoid a hook in a specific file you
can add a comment somewhere in the file saying so. For example::

 # hghooks: no-pyflakes no-pdb

in this case the pyflakes and pdb hooks will skip this file. The
"``# hghooks:``" prolog is important and you have to type it exactly
like that. Then add the skip keyworkds separated by spaces.
