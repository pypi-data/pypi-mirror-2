.. contents:: Table of Contents
   :depth: 2

sc.paster.policy
****************

Introduction
------------

`sc.paster.policy <http://www.simplesconsultoria.com.br>`_ -- is a paster 
template used to create a buildout for a Plone project.

It's intended to be used on Simples Consultoria's Plone projects so it contains 
some idiosyncrasies related to our internal needs.

Installation
------------

If you have installed `setuptools
<http://pypi.python.org/pypi/setuptools>`_ or `distribute
<http://pypi.python.org/pypi/distribute>`_ an ``easy_install``
command will be available.  Then, you can install sc.paster.policy using
``easy_install`` command like this::

  $ easy_install -U sc.paster.buildout

Internet access to `PyPI <http://pypi.python.org/pypi>`_ is required
to perform installation of sc.paster.buildout.

Usage
-----

After install just type

::

  $ paster create -t portal_buildout buildout

in order to bring a wizard to help you setup this new portal policy.

We recommend you to already import this buildout to a vcs repository. To do so, 
using svn, just add the switch --svn-repository to the paster command line

::

  $ paster create -t portal_buildout buildout 
  --svn-repository=https://dev.plone.org/svn/collective/
  
This command will create the package code tree under 
https://dev.plone.org/svn/collective/

Sponsoring
----------

Development of this product was sponsored by `Simples Consultoria 
<http://www.simplesconsultoria.com.br/>`_.


Credits
-------
    
    * Erico Andrei (erico at simplesconsultoria dot com dot br) - Packaging, 
      plumbing.
