``repoze.bfg`` bindings for `Mako <http://www.makotemplates.org/>`_
===================================================================

These are bindings for the `Mako templating system
<http://www.makotemplates.org/>`_ for the `repoze.bfg
<http://bfg.repoze.org/`_ web framework.

High-Level API
--------------

The API follows the pattern of the "default" template API for
``repoze.bfg``, which includes three functions: ``get_template``,
``render_template``, and ``render_template_to_response``.  From within
a repoze.bfg view function, you might do::

  from webob import Response

  from repoze.bfg.renderers import get_renderer
  template = get_renderer('templates/foo.mak')
  return Response(template.render_unicode(foo=1))

Or::

  from repoze.bfg.renderers import render
  s = render('templates/foo.mak', {foo:1})
  return Response(s)

Or::

  from repoze.bfg.renderers import render_to_response
  return render_to_response('templates/foo.mak', {foo:1})

All of these examples are equivalent.  The first argument passed in to
each of them (representing the template location) should be a file
path relative to the lookup loader root.

Configuring the Loookup Loader
------------------------------

In your bfg application's ``.ini`` file, use a ``mako.directories``
setting::

  [app:main]
  use = egg:mypackage
  mako.directories = mypackage:templates
                     anotherpackage:templates
  reload_templates = true
  debug_authorization = false
  debug_notfound = false

``mako.directories`` should be a sequence of absolute directory names
or resource specifications, one per line.

Other values:

``mako.input_encoding``
   Set the mako template input encoding.  The default is ``utf-8``.

``reload_templates``
   If this is ``True``, Mako templates will be checked for changes at
   every rendering boundary.  This slows down rendering but is
   convenient for development.

Ensuring the Mako Renderer Extension is Active
----------------------------------------------

``repoze.bfg.mako`` can also act as a "renderer" for a view when it is
active in the ``repoze.bfg`` application you're developing::

  @bfg_view(renderer='templates/foo.mak')
  def aview(request):
      return {'foo':1}

There are two ways to make sure that the mako extension is active.
Both are completely equivalent.

#) Ensure that some ZCML file with an analogue of the following
   contents is executed::

    <include package="repoze.bfg.mako"/>

#) Call the ``add_renderer`` method of a Configurator in your
   application:

   from repoze.bfg.mako import renderer_factory
   config.add_renderer(.'mak', renderer_factory)
   config.add_renderer(.'mako', renderer_factory)

In either case, files with the ``.mak`` and ``.mako`` extensions are
now considered to be Mako templates.

Note that when mako is used as a ``renderer`` in this fashion, the
``repoze.bfg`` context that is usually available as ``context`` within
the template global namespace is available as ``_context`` (the
``context`` name without the underscore is reserved for internal Mako
usage).

Installation
------------

Install using setuptools, e.g. (within a virtualenv)::

  $ easy_install -i http://dist.repoze.org/bfg/dev/simple repoze.bfg.mako

Creating a Mako ``repoze.bfg`` Project
--------------------------------------

After you've got ``repoze.bfg.mako`` installed, you can invoke the
following command to create a Mako-based ``repoze.bfg`` project::

  $ paster create -t bin/paster create -t bfg_mako_starter

Reporting Bugs / Development Versions
-------------------------------------

Visit http://bugs.repoze.org to report bugs.  Visit
http://svn.repoze.org to download development or tagged versions.


