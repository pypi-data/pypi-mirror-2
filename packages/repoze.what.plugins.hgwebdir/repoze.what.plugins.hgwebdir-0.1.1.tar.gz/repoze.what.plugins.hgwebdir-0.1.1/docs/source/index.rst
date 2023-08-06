======================================
The :mod:`repoze.what` Hgwebdir plugin
======================================

:Author: Yaco Sistemas (Lorenzo Gil)
:Latest release: |release|

.. module:: repoze.what.plugins.hgwebdir
    :synopsis: Ready-to-use authentication and authorization
.. moduleauthor:: Lorenzo Gil <lgs@yaco.es>

.. topic:: Overview

   This plugin allows to override the hgwebdir authorization support with
   a more sophisticated one that allows more flexibility and maintainability.

   It allows to define your repository access information in a single file
   and has some utility functions to protect a wsgi application like
   Mercurial include hgwebdir.

How to install
==============

The minimum requirements are :mod:`repze.what` and you can install it all
with ``easy_install``::

  easy_install repoze.what.plugins.hgwebdir

The development mainline is available at the following Mercurial repository::

  hg clone http://bitbucket.org/lgs/repoze.what.plugins.hgwebdir

How to get help
===============

The prefered place to ask questions is the #yaco.es `#yaco.es
<irc://irc.freenode.net/#repoze>`_ IRC channel. Bugs reports and feature
requests should be sent to `the issue tracker of Bitbucket
<http://bitbucket.org/lgs/repoze.what.plugins.hgwebdir/issues?status=new&status=open>`_.

How to use it
=============

This plugin includes a repoze.what Group source, a Permission source, a couple
of predicate checkers and an utility middleware to protect the hgwebdir
application.

Group and permission sources
----------------------------

The group and permission sources are based on Subversion mod_authz_svn and they
both use a single file very similar to the one Subversion uses. This file
is a ini like configuration file where you have sections and inside them,
you have options and values.

The first section is a special one called ``groups``. In this section
you define the groups of users that you have. To define a group put the
name of the group as the option name and the user names of the members of
such groups as the value. The members is a list of user ids separated by
spaces and (optionally) commas.

Let's see an example::

 [groups]
 rolling = mick, keith, ronnie, charlie
 beatles = john, paul, george, ringo

Here you have two groups, each one having four members.

After the groups section you will have a section for each Mercurial
repository you want to serve. If you have a repository and it is not
listed on this file the default behaviour is to forbid any access to it.

So you have a section for each repository. Inside the section you define who
can access to it. There are basically two operations on a repository, reading
it or writing to it. So each option inside a repository will define who
can read or write it. A option starting with ``@`` references the name of
a group (from the groups section). A option without the ``@`` means just
a user id. An ``*`` means ``everybody``. The value can be ``r``, ``w`` or
``rw`` if you want to give read, write or read and write access respectively.

Let's see another example::

 [sticky-fingers]
 @rolling = rw
 @beatles = r

 [sargent-peppers]
 @beatles = rw
 @rolling = r

 [pet-sounds]
 * = r

Here there are three repositories: ``sticky-fingers``, ``sargent-peppers``
and ``pet-sounds``. In the ``sticky-fingers`` repository the members of the
``rolling`` group have read and write permissions while the members of the
``beatles`` group have only read permissions. In the ``sargent-peppers``
repository is the other way around and lastly, in the ``pet-sounds``
repository, everybody have read access and nobody can write.

Now you are ready to use the HgwebdirGroupsAdapter and the
HgwebdirPermissionsAdapter. The only thing both of these classes need is
the path to your authz file. Theorically you can instantiate each of
these classes with a different auth file but in practice that doesn't make
much sense.

Let's see a full example of how o integrate these sources with the rest
of repoze.what and repoze.who funcionality::

 from repoze.who.plugins.basicauth import BasicAuthPlugin
 from repoze.who.plugins.htpasswd import HTPasswdPlugin, crypt_check
 from repoze.what.middleware import setup_auth

 from repoze.what.plugins.hgwebdir.adapters import HgwebdirGroupsAdapter
 from repoze.what.plugins.hgwebdir.adapters import HgwebdirPermissionsAdapter


 def add_auth(app, users_file, authz_file):
     """
     Add authentication and authorization middleware to the ``app``.

     :param app: The WSGI application.
     :param users_file: a httpasswd file with users and passwords
     :param authz_file: an ini file with group and permissions
     :return: The same WSGI application, with authentication and
         authorization middleware.

     """
     groups = {'all_groups': HgwebdirGroupsAdapter(authz_file)}

     permissions = {'all_perms': HgwebdirPermissionsAdapter(authz_file)}

     basicauth = BasicAuthPlugin('Your realm')
     identifiers = [('basicauth', basicauth)]

     htpasswd_auth = HTPasswdPlugin(users_file, crypt_check)
     authenticators = [('htpasswd_auth', htpasswd_auth)]

     challengers = [('basicauth', basicauth)]

     app_with_auth = setup_auth(
         app,
         groups,
         permissions,
         identifiers=identifiers,
         authenticators=authenticators,
         challengers=challengers)
     return app_with_auth

In the repoze.what.plugins.hgwebdir.adapters module ther is another
function called ``get_public_repositories``. It needs the path to the
authz file and will return a list of repository names that are public. A
repository is public if it has at least an option like ``* = r``. In the
above example this function would return a list with one element, the
``pet-sounds`` repository::

 >>> from repoze.what.plugins.hgwebdir.adapters import get_public_repositories

 >>> get_public_repositories('/path/to/authz.ini')
 [u'pet-sounds']


Predicate checkers
------------------

This plugin has two new predicate checkers: ``is_read_access`` and
``has_repo_access``.

The ``is_read_access`` predicate checker is quite simple since it does not
need any parameter in its constructor and it just check whetever the request
is using a GET http verb or not::

 from repoze.what.plugins.hgwebdir.predicates import is_read_access

 p = is_read_access()

The other predicate checker, ``has_repo_access`` is quite more interesting.
It is a compuound predicate checker that test several things. It needs the
name of the repository it is trying to protect and It will allow
access to such resource if any of the following assertions is true:

* The request is a read action and the user has the permission made from the
  name of the repository plus the string ``-read``. For example, if the
  repository is called ``project23`` the user will need the permission
  ``project23-read``.
* The request is not a read action and the user has the permission made from
  the name of the repository plus the string ``-write``. For example, if the
  repository is called ``project23`` the user will need the permission
  ``project23-write``.
* The request is a read action and the repository is public.

This predicate checker has two construction parameters:

* ``repo_name``: the name of the repository
* ``public_repos``: a list of repository names that are public

Let's see an example of its use::

 from repoze.what.plugins.hgwebdir.predicates import has_repo_access

 p = has_repo_access('project12', ['public-project1', 'public-project2'])


Middleware
----------

In the middleware land of this plugin you will find a single function, the
``protect_repositories`` callable. Give it the wsgi application that
is returned by the mercurial.hgweb.hgwebdir_mod.hgwebdir function and
it will add authorization support by using the ``has_repo_access`` predicate
checker that is explained above.

The second argument to the ``protect_repositories`` function is a list
of public repositories. These repositories should be granted read access
to everybody.

As you can see this function ties everything together into a useful piece
of middleware. Let's see an example of its use::

 from mercurial.hgweb.hgwebdir_mod import hgwebdir

 from repoze.what.plugins.hgwebdir.adapters import get_public_repositories
 from repoze.what.plugins.hgwebdir.middleware import protect_repositories

 def make_app(hg_config, users_file, authz_file):
     original_app = hgwebdir(hg_config)
     secured_app = protect_repositories(original_app,
                                        get_public_repositories(authz_file))
     return add_auth(secured_app, users_file, authz_file)


The ``add_auth`` function was explained in the Group and Permissions sources
section.


Contents:
=========

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

