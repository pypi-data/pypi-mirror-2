.. contents::

============================
repoze.what.plugins.hgwebdir
============================

repoze.what.plugins.hgwebdir is a repoze.what plugin suitable to be used
when serving Mercurial repositories through the wsgi application bundled
with Mercurial, hgwebdir.

The basic advantage of using this plugin instead of hgwebdir authorization
mechanisms is that you can put all your authorization information for multiple
repositories in a single file. The format and purpose of this file is
inspired in the one that the mod_authz_svn Apache module uses. This plugin
makes a little bit easier to migrate from Subverion to Mercurial in
enterprise like environments.

This plugin is distributed with the same license as repoze.what, e.g. a
BSD like license.

Check the http://www.lorenzogil.com/projects/repoze.what.plugins.hgwebdir/
website for the full documentation.

