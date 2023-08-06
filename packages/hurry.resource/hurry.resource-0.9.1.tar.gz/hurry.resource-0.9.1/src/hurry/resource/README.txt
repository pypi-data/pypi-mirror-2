hurry.resource
**************

Introduction
============

Resources are files that are used as resources in the display of a web
page, such as CSS files, Javascript files and images. Resources
packaged together in a directory to be published as such are called a
resource *library*.

When a resource is included in the ``head`` section of a HTML page, we
call this a resource *inclusion*. An inclusion is of a particular
resource in a particular library. There are two forms of this kind of
inclusion in HTML: javascript is included using the ``script`` tag,
and CSS (and KSS) are included using a ``link`` tag.

Inclusions may depend on other inclusions. A javascript resource may
for instance be built on top of another javascript resource. This
means both of them should be loaded when the page displays.

Page components may actually require a certain inclusion in order to
be functional. A widget may for instance expect a particular
Javascript library to loaded. We call this an *inclusion requirement*
of the component.

``hurry.resource`` provides a simple API to specify resource
libraries, inclusion and inclusion requirements.

A resource library
==================

We define a library ``foo``::

  >>> from hurry.resource import Library
  >>> foo = Library('foo')

Inclusion
=========

We now create an inclusion of a particular resource in a library. This
inclusion needs ``a.js`` from ``library`` and ``b.js`` as well::

  >>> from hurry.resource import ResourceInclusion
  >>> x1 = ResourceInclusion(foo, 'a.js')
  >>> x2 = ResourceInclusion(foo, 'b.css')

Let's now make an inclusion ``y1`` that depends on ``x1`` and ``x2``::

  >>> y1 = ResourceInclusion(foo, 'c.js', depends=[x1, x2])

Inclusion requirements
======================

When rendering a web page we want to require the inclusion of a
resource anywhere within the request handling process. We might for
instance have a widget that takes care of rendering its own HTML but
also needs a resource to be included in the page header.

We have a special object that represents the needed inclusions during
a certain request cycle::

  >>> from hurry.resource import NeededInclusions
  >>> needed = NeededInclusions()

We state that a resource is needed by calling the ``need`` method on
this object::

  >>> needed.need(y1)

Let's now see what resources are needed by this inclusion::

  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

As you can see, ``css`` resources are sorted before ``js`` resources.

Grouping resources
==================

It is also possible to define a group that doesn't get rendered
itself, but groups other resources together that should be rendered::

  >>> from hurry.resource import GroupInclusion
  >>> group = GroupInclusion([x1, x2])

When we need a group, we'll get all inclusions referenced in it::

  >>> needed = NeededInclusions()
  >>> needed.need(group)
  >>> group.inclusions()
  [<ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'b.css' in library 'foo'>]

A group can also be depended on; it won't show up in the list of
inclusions directly::

  >>> more_stuff = ResourceInclusion(foo, 'more_stuff.js', depends=[group])
  >>> more_stuff.inclusions()
  [<ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'b.css' in library 'foo'>,
   <ResourceInclusion 'more_stuff.js' in library 'foo'>]

A convenience spelling
======================

When specifying that we want a resource inclusion to be rendered, we
now need access to the current ``NeededInclusions`` object and the
resource inclusion itself.

Let's introduce a more convenient spelling of needs now::

  y1.need()

We can require a resource without reference to the needed inclusions
object directly as there is typically only a single set of needed
inclusions that is generated during the rendering of a page.  

So let's try out this spelling to see it fail::

  >>> y1.need()
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass hurry.resource.interfaces.ICurrentNeededInclusions>, '')

We get an error because we haven't configured the framework yet. The
system says it cannot find the utility component
``ICurrentNeededInclusions``. This is the utility we need to define
and register so we can tell the system how to obtain the current
``NeededInclusions`` object. Our task is therefore to provide a
``ICurrentNeededInclusions`` utility that can give us the current
needed inclusions object.

This needed inclusions should be maintained on an object that is going
to be present throughout the request/response cycle that generates the
web page that has the inclusions on them. The most obvious place where
we can maintain the needed inclusions is the request object
itself. Let's introduce such a simple request object (your mileage may
vary in your own web framework)::

  >>> class Request(object):
  ...    def __init__(self):
  ...        self.needed = NeededInclusions()

We now make a request, imitating what happens during a typical
request/response cycle in a web framework::

  >>> request = Request()

We should define a ``ICurrentNeededInclusion`` utility that knows how
to get the current needed inclusions from that request::

  >>> def currentNeededInclusions():
  ...    return request.needed

  >>> c = currentNeededInclusions

We need to register the utility to complete plugging into the
``INeededInclusions`` pluggability point of the ``hurry.resource``
framework::

  >>> from zope import component
  >>> from hurry.resource.interfaces import ICurrentNeededInclusions
  >>> component.provideUtility(currentNeededInclusions, 
  ...     ICurrentNeededInclusions)

Let's check which resources our request needs currently::

  >>> c().inclusions()
  []

Nothing yet. We now make ``y1`` needed using our simplified spelling::

  >>> y1.need()

The resource inclusion will now indeed be needed::

  >>> c().inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

In this document we already have a handy reference to ``c`` to obtain
the current needed inclusions, but that doesn't work in a larger
codebase. How do we get this reference back, for instance to obtain those
resources needed? Here is how you can obtain a utility by hand::

  >>> c_retrieved = component.getUtility(ICurrentNeededInclusions)
  >>> c_retrieved is c
  True

Let's go back to the original spelling of ``needed.need(y)``
now. While this is a bit more cumbersome to use in application code, it is
easier to read for the purposes of this document.

A note on optimization
======================

There are various optimizations for resource inclusion that
``hurry.resource`` supports. Because some optimizations can make
debugging more difficult, the optimizations are disabled by default.

We will summarize the optimization features here and tell you how to
enable them. Later sections below go into more details.

* minified resources. Resources can specify minified versions using
  the mode system. You can use ``hurry.resource.mode('minified')``
  somewhere in the request handling of your application. This will
  make sure that resources included on your page are supplied as
  minified versions, if these are available. 

* rolling up of resources.  Resource libraries can specify rollup
  resources that combine multiple resources into one. This reduces the
  amount of server requests to be made by the web browser, and can
  help with caching. To enable rolling up, call
  ``hurry.resource.rollup`` somewhere in your request handling.

* javascript inclusions at the bottom of the web page. If your
  framework integration uses the special ``render_topbottom`` method,
  you can enable the inclusion of javascript files at the bottom by
  calling ``hurry.resource.bottom()``. This will only include
  resources at the bottom that have explicitly declared themselves to
  be *bottom-safe*. You can declare a resource bottom safe by passing
  ``bottom=True`` when constructing a ``ResourceInclusion``. If you
  want to force all javascript to be including at the bottom of the
  page by default, you can call ``hurry.resource.bottom(force=True)``.

To find out more about these and other optimizations, please read this
`best practices article`_ that describes some common optimizations to
speed up page load times.

.. _`best practices article`: http://developer.yahoo.com/performance/rules.html

Multiple requirements
=====================

In this section, we will show what happens in various scenarios where
we requiring multiple ``ResourceInclusion`` objects.

We create a new set of needed inclusions::

  >>> needed = NeededInclusions()
  >>> needed.inclusions()
  []

We need ``y1`` again::

  >>> needed.need(y1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

Needing the same inclusion twice won't make any difference for the
resources needed. So when we need ``y1`` again, we see no difference
in the needed resources::

  >>> needed.need(y1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

Needing ``x1`` or ``x2`` won't make any difference either, as ``y1``
already required ``x1`` and ``x2``::

  >>> needed.need(x1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]
  >>> needed.need(x2)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

Let's do it in reverse, and require the ``x1`` and ``x2`` resources
before we need those in ``y1``. Again this makes no difference::

  >>> needed = NeededInclusions()
  >>> needed.need(x1)
  >>> needed.need(x2)
  >>> needed.need(y1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>,
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

Let's try it with more complicated dependency structures now::

  >>> needed = NeededInclusions()
  >>> a1 = ResourceInclusion(foo, 'a1.js')
  >>> a2 = ResourceInclusion(foo, 'a2.js', depends=[a1])
  >>> a3 = ResourceInclusion(foo, 'a3.js', depends=[a2])
  >>> a4 = ResourceInclusion(foo, 'a4.js', depends=[a1])
  >>> needed.need(a3)
  >>> needed.inclusions()
  [<ResourceInclusion 'a1.js' in library 'foo'>,
   <ResourceInclusion 'a2.js' in library 'foo'>,
   <ResourceInclusion 'a3.js' in library 'foo'>]
  >>> needed.need(a4)
  >>> needed.inclusions()
  [<ResourceInclusion 'a1.js' in library 'foo'>,
   <ResourceInclusion 'a2.js' in library 'foo'>,
   <ResourceInclusion 'a3.js' in library 'foo'>,
   <ResourceInclusion 'a4.js' in library 'foo'>]

If we reverse the requirements for ``a4`` and ``a3``, we get the following
inclusion structure, based on the order in which need was expressed::

  >>> needed = NeededInclusions()
  >>> needed.need(a4)
  >>> needed.need(a3)
  >>> needed.inclusions()
  [<ResourceInclusion 'a1.js' in library 'foo'>,
   <ResourceInclusion 'a4.js' in library 'foo'>,
   <ResourceInclusion 'a2.js' in library 'foo'>,
   <ResourceInclusion 'a3.js' in library 'foo'>]

Let's look at the order in which resources are listed when we need
something that ends up depending on everything::

  >>> a5 = ResourceInclusion(foo, 'a5.js', depends=[a4, a3])
  >>> needed = NeededInclusions()
  >>> needed.need(a5)
  >>> needed.inclusions()
  [<ResourceInclusion 'a1.js' in library 'foo'>,
   <ResourceInclusion 'a4.js' in library 'foo'>,
   <ResourceInclusion 'a2.js' in library 'foo'>,
   <ResourceInclusion 'a3.js' in library 'foo'>,
   <ResourceInclusion 'a5.js' in library 'foo'>]

When we introduce the extra inclusion of ``a3`` earlier on, we still
get a valid list of inclusions given the dependency structure, even
though the sorting order is different::

  >>> needed = NeededInclusions()
  >>> needed.need(a3)
  >>> needed.need(a5)
  >>> needed.inclusions()
  [<ResourceInclusion 'a1.js' in library 'foo'>, 
   <ResourceInclusion 'a2.js' in library 'foo'>, 
   <ResourceInclusion 'a3.js' in library 'foo'>, 
   <ResourceInclusion 'a4.js' in library 'foo'>, 
   <ResourceInclusion 'a5.js' in library 'foo'>]

Modes
=====

A resource can optionally exist in several modes, such as for instance
a minified and a debug version. Let's define a resource that exists in
two modes (a main one and a debug alternative)::

  >>> k1 = ResourceInclusion(foo, 'k.js', debug='k-debug.js')

Let's need this resource::

  >>> needed = NeededInclusions()
  >>> needed.need(k1)

By default, we get ``k.js``::

  >>> needed.inclusions()
  [<ResourceInclusion 'k.js' in library 'foo'>]

We can however also get the resource for mode ``debug`` and get
``k-debug.js``::

  >>> needed.mode('debug')
  >>> needed.inclusions()
  [<ResourceInclusion 'k-debug.js' in library 'foo'>]

Modes can also be specified fully with a resource inclusion, which allows
you to specify a different ``library`` argumnent::

  >>> k2 = ResourceInclusion(foo, 'k2.js', 
  ...                        debug=ResourceInclusion(foo, 'k2-debug.js'))
  >>> needed = NeededInclusions()
  >>> needed.need(k2)

By default we get ``k2.js``::

  >>> needed.inclusions()
  [<ResourceInclusion 'k2.js' in library 'foo'>]

We can however also get the resource for mode ``debug`` and get
``k2-debug.js``::

  >>> needed.mode('debug')
  >>> needed.inclusions()
  [<ResourceInclusion 'k2-debug.js' in library 'foo'>]

Note that modes are assumed to be identical in dependency structure;
they functionally should do the same.

If you request a mode and a resource doesn't support it, it will
return its default resource instead::

  >>> needed = NeededInclusions()
  >>> needed.mode('minified')
  >>> needed.need(k1)
  >>> needed.inclusions()
  [<ResourceInclusion 'k.js' in library 'foo'>]

``hurry.resource`` suggests resource libraries follow the following
conventions for modes:

  * default - the original source text, non-minified, and without any
    special extra debugging functionality.

  * debug - an optional version of the source text that offers more
    debugging support, such as logging.

  * minified - an optional minified (compressed) form of the resource.

In the case of rollups, several resources can be consolidated into one
larger one for optimization purposes. A library might only offer a
minified version of a rollup resource; if the developer wants to
debug, it is expected he uses the resources in non-rolledup format.
In this case you should make a resource inclusion where the default
mode is equal to the minified mode, like this::

  >>> example = ResourceInclusion(foo, 'k.js', minified='k.js')

If the developer wants to debug, he will need to disable rolling up
(by calling ``hurry.resource.rollup(disable=True)``, or by simply
never calling ``hurry.resource.rollup()`` in the request cycle).

Mode convenience
================

Like for ``need``, there is also a convenience spelling for
``mode``. It uses ``ICurrentNeededInclusions``, which we've already
set up to look at the ``request.needed`` variable. Let's set up
a new request::

  >>> request = Request()

Let's set up a resource and need it::

  >>> l1 = ResourceInclusion(foo, 'l1.js', debug='l1-debug.js')
  >>> l1.need()

Let's look at the resources needed by default::

  >>> c = component.getUtility(ICurrentNeededInclusions)
  >>> c().inclusions()
  [<ResourceInclusion 'l1.js' in library 'foo'>]

Let's now change the mode using the convenience
``hurry.resource.mode`` spelling::

  >>> from hurry.resource import mode
  >>> mode('debug')

When we request the resources now, we get them in the ``debug`` mode::

  >>> c().inclusions()
  [<ResourceInclusion 'l1-debug.js' in library 'foo'>]

"Rollups"
=========

For performance reasons it's often useful to consolidate multiple
resources into a single, larger resource, a so-called
"rollup". Multiple javascript files could for instance be offered in a
single, larger one. These consolidations can be specified as a
resource::

  >>> b1 = ResourceInclusion(foo, 'b1.js')
  >>> b2 = ResourceInclusion(foo, 'b2.js')
  >>> giant = ResourceInclusion(foo, 'giant.js', supersedes=[b1, b2])

Rolling up of resources is not enabled by default, as sometimes a
library only offers these rollups in minified form, and automatically
rolling up would not be nice during debugging. It's therefore a
performance feature you can enable.

Without rollups enabled nothing special happens::

  >>> needed = NeededInclusions()
  >>> needed.need(b1)
  >>> needed.need(b2)
  >>> needed.inclusions()
  [<ResourceInclusion 'b1.js' in library 'foo'>, <ResourceInclusion 'b2.js' in library 'foo'>]

Let's enable rollups::

  >>> needed = NeededInclusions()
  >>> needed.rollup()

The convenience spelling to enable rollups during request handling
looks like this::

  hurry.resource.rollup()

If we now find multiple resources that are also part of a
consolidation, the system automatically collapses them::

  >>> needed.need(b1)
  >>> needed.need(b2)
  >>> needed.inclusions()
  [<ResourceInclusion 'giant.js' in library 'foo'>]

The system will by default only consolidate exactly. That is, if only a single
resource out of two is present, the consolidation will not be triggered::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(b1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b1.js' in library 'foo'>]

Let's look at this with a larger consolidation of 3 resources::

  >>> c1 = ResourceInclusion(foo, 'c1.css')
  >>> c2 = ResourceInclusion(foo, 'c2.css')
  >>> c3 = ResourceInclusion(foo, 'c3.css')
  >>> giantc = ResourceInclusion(foo, 'giantc.css', supersedes=[c1, c2, c3])
 
It will not roll up one resource::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(c1)
  >>> needed.inclusions()
  [<ResourceInclusion 'c1.css' in library 'foo'>]

Neither will it roll up two resources::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(c1)
  >>> needed.need(c2)
  >>> needed.inclusions()
  [<ResourceInclusion 'c1.css' in library 'foo'>,
   <ResourceInclusion 'c2.css' in library 'foo'>]
  
It will however roll up three resources::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(c1)
  >>> needed.need(c2)
  >>> needed.need(c3)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantc.css' in library 'foo'>]

The default behavior is to play it safe: we cannot be certain that we
do not include too much if we were to include ``giantc.css`` if only
c1 and c2 are required. This is especially important with CSS
libraries: if only ``c1.css`` and ``c2.css`` are to be included in a
page, including ``giantc.css`` is not appropriate as that also
includes the content of ``c3.css``, which might override and extend
the behavior of ``c1.css`` and ``c2.css``.

The situation is sometimes different with Javascript libraries, which
can be written in such a way that a larger rollup will just include
more functions, but will not actually affect page behavior. If we have
a rollup resource that we don't mind kicking in even if part of the
requirements have been met, we can indicate this::

  >>> d1 = ResourceInclusion(foo, 'd1.js')
  >>> d2 = ResourceInclusion(foo, 'd2.js')
  >>> d3 = ResourceInclusion(foo, 'd3.js')
  >>> giantd = ResourceInclusion(foo, 'giantd.js', supersedes=[d1, d2, d3],
  ...            eager_superseder=True)

We will see ``giantd.js`` kick in even if we only require ``d1`` and
``d2``::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(d1)
  >>> needed.need(d2)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantd.js' in library 'foo'>]

In fact even if we only need a single resource the eager superseder will
show up instead::

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(d1)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantd.js' in library 'foo'>]

If there are two potential eager superseders, the biggest one will
be taken::

  >>> d4 = ResourceInclusion(foo, 'd4.js')
  >>> giantd_bigger = ResourceInclusion(foo, 'giantd-bigger.js', 
  ...   supersedes=[d1, d2, d3, d4], eager_superseder=True)
  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(d1)
  >>> needed.need(d2)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantd-bigger.js' in library 'foo'>]

If there is a potential non-eager superseder and an eager one, the eager one
will be taken::

  >>> giantd_noneager = ResourceInclusion(foo, 'giantd-noneager.js',
  ...   supersedes=[d1, d2, d3, d4])
  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(d1)
  >>> needed.need(d2)
  >>> needed.need(d3)
  >>> needed.need(d4)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantd-bigger.js' in library 'foo'>]

A resource can be part of multiple rollups. In this case the rollup
that rolls up the most resources is used. So, if there are two
potential non-eager superseders, the one that rolls up the most
resources will be used::
 
  >>> e1 = ResourceInclusion(foo, 'e1.js')
  >>> e2 = ResourceInclusion(foo, 'e2.js')
  >>> e3 = ResourceInclusion(foo, 'e3.js')
  >>> giante_two = ResourceInclusion(foo, 'giante-two.js',
  ...   supersedes=[e1, e2])
  >>> giante_three = ResourceInclusion(foo, 'giante-three.js',
  ...   supersedes=[e1, e2, e3])
  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(e1)
  >>> needed.need(e2)
  >>> needed.need(e3)
  >>> needed.inclusions()
  [<ResourceInclusion 'giante-three.js' in library 'foo'>]

Consolidation also works with modes::

  >>> f1 = ResourceInclusion(foo, 'f1.js', debug='f1-debug.js')
  >>> f2 = ResourceInclusion(foo, 'f2.js', debug='f2-debug.js')
  >>> giantf = ResourceInclusion(foo, 'giantf.js', supersedes=[f1, f2],
  ...                            debug='giantf-debug.js')

  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(f1)
  >>> needed.need(f2)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantf.js' in library 'foo'>]
  >>> needed.mode('debug')
  >>> needed.inclusions()
  [<ResourceInclusion 'giantf-debug.js' in library 'foo'>]

What if the rolled up resources have no mode but the superseding resource
does? In this case the superseding resource's mode has no meaning, so
modes have no effect::

  >>> g1 = ResourceInclusion(foo, 'g1.js')
  >>> g2 = ResourceInclusion(foo, 'g2.js')
  >>> giantg = ResourceInclusion(foo, 'giantg.js', supersedes=[g1, g2],
  ...                            debug='giantg-debug.js')
  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(g1)
  >>> needed.need(g2)
  >>> needed.inclusions()
  [<ResourceInclusion 'giantg.js' in library 'foo'>]
  >>> needed.mode('debug')
  >>> needed.inclusions()
  [<ResourceInclusion 'giantg.js' in library 'foo'>]

What if the rolled up resources have a mode but the superseding resource
does not? Let's look at that scenario::

  >>> h1 = ResourceInclusion(foo, 'h1.js', debug='h1-debug.js')
  >>> h2 = ResourceInclusion(foo, 'h2.js', debug='h2-debug.js')
  >>> gianth = ResourceInclusion(foo, 'gianth.js', supersedes=[h1, h2])
  >>> needed = NeededInclusions()
  >>> needed.rollup()
  >>> needed.need(h1)
  >>> needed.need(h2)
  >>> needed.inclusions()
  [<ResourceInclusion 'gianth.js' in library 'foo'>]

Since there is no superseder for the debug mode, we will get the two 
resources, not rolled up::

  >>> needed.mode('debug')
  >>> needed.inclusions()
  [<ResourceInclusion 'h1-debug.js' in library 'foo'>,
   <ResourceInclusion 'h2-debug.js' in library 'foo'>]

Rendering resources
===================

Let's define some needed resource inclusions::

  >>> needed = NeededInclusions()
  >>> needed.need(y1)
  >>> needed.inclusions()
  [<ResourceInclusion 'b.css' in library 'foo'>, 
   <ResourceInclusion 'a.js' in library 'foo'>, 
   <ResourceInclusion 'c.js' in library 'foo'>]

Now let's try to render these inclusions::

  >>> print needed.render()
  Traceback (most recent call last):
    ...
  TypeError: ('Could not adapt', <hurry.resource.core.Library object at ...>, <InterfaceClass hurry.resource.interfaces.ILibraryUrl>)

That didn't work. In order to render an inclusion, we need to tell
``hurry.resource`` how to get the URL for a resource inclusion. We
already know the relative URL, so we need to specify how to get a URL
to the library itself that the relative URL can be added to.

For the purposes of this document, we define a function that renders
resources as some static URL on localhost::

  >>> def get_library_url(library):
  ...    return 'http://localhost/static/%s' % library.name

We should now register this function as a``ILibraryUrl`` adapter for
``Library`` so the system can find it::

  >>> from hurry.resource.interfaces import ILibraryUrl
  >>> component.provideAdapter(
  ...     factory=get_library_url,
  ...     adapts=(Library,), 
  ...     provides=ILibraryUrl)

Rendering the inclusions now will result in the HTML fragments we
need to include on the top of our page (just under the ``<head>`` tag
for instance)::

  >>> print needed.render()
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>

Let's set this a currently needed inclusions::
  
  >>> request.needed = needed

There is a function available as well for rendering the resources for
the currently needed inclusion::

  >>> from hurry import resource
  >>> print resource.render()
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>

Inserting resources in HTML
===========================

When you have the HTML it can be convenient to have a way to insert
resources directly into some HTML. 

The insertion system assumes a HTML text that has a ``<head>`` tag in it::

  >>> html = "<html><head>something more</head></html>"

To insert the resources directly in HTML we can use ``render_into_html``
on ``needed``::

  >>> print needed.render_into_html(html)
  <html><head>
      <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  something more</head></html>

The top-level convenience function does this for the currently needed
resources::

  >>> print resource.render_into_html(html)
  <html><head>
      <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  something more</head></html>

See below for a way to insert into HTML when bottom fragments are
involved.

Top and bottom fragments
========================

It's also possible to render the resource inclusions into two
fragments, some to be included just after the ``<head>`` tag, but some
to be included at the very bottom of the HTML page, just before the
``</body>`` tag. This is useful as it can `speed up page load times`_. 

.. _`speed up page load times`: http://developer.yahoo.com/performance/rules.html

Let's look at the same resources, now rendered separately into ``top``
and ``bottom`` fragments::

  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  >>> print bottom
  <BLANKLINE>

There is effectively no change; all the resources are still on the
top. We can enable bottom rendering by calling the ``bottom`` method before
we render::

  >>> needed.bottom()

Since none of the resources indicated it was safe to render them at
the bottom, even this explicit call will not result in any changes::
 
  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  >>> print bottom
  <BLANKLINE>

``bottom(force=True)`` will however force all javascript inclusions to be
rendered in the bottom fragment::

  >>> needed.bottom(force=True)
  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  >>> print bottom
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>

Let's now introduce a javascript resource that says it is safe to be
included on the bottom::
 
  >>> y2 = ResourceInclusion(foo, 'y2.js', bottom=True)

When we start over without ``bottom`` enabled, we get this resource
show up in the top fragment after all::

  >>> needed = NeededInclusions()
  >>> needed.need(y1)
  >>> needed.need(y2)

  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script>
  >>> print bottom
  <BLANKLINE>

We now tell the system that it's safe to render inclusions at the bottom::

  >>> needed.bottom()

We now see the resource ``y2`` show up in the bottom fragment::

  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  >>> print bottom
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script>

There's also a convenience function for the currently needed inclusion::

  >>> request.needed = needed
  >>> top, bottom = resource.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  >>> print bottom
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script>

When we force bottom rendering of Javascript, there is no effect of
making a resource bottom-safe: all ``.js`` resources will be rendered
at the bottom anyway::

  >>> needed.bottom(force=True)
  >>> top, bottom = needed.render_topbottom()
  >>> print top
  <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  >>> print bottom
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script>

Note that if ``bottom`` is enabled, it makes no sense to have a
resource inclusion ``b`` that depends on a resource inclusion ``a``
where ``a`` is bottom-safe and ``b``, that depends on it, is not
bottom-safe. In this case ``a`` would be included on the page at the
bottom *after* ``b`` in the ``<head>`` section, and this might lead to
ordering problems. Likewise a rollup resource shouldn't combine
resources where some are bottom-safe and others aren't.

The system makes no sanity checks for misconfiguration of
bottom-safety however; it could be the user simply never enables
``bottom`` mode at all and doesn't care about this issue. In this case
the user will want to write Javascript code that isn't safe to be
included at the bottom of the page and still be able to depend on
Javascript code that is.

Inserting top and bottom resources in HTML
==========================================

You can also insert top and bottom fragments into HTML. This assumes a
HTML text that has a ``<head>`` tag in it as well as a ``</body>``
tag::

  >>> html = "<html><head>rest of head</head><body>rest of body</body></html>"

To insert the resources directly in HTML we can use
``render_topbottom_into_html`` on ``needed``::

  >>> print needed.render_topbottom_into_html(html)
  <html><head>
      <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  rest of head</head><body>rest of body<script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script></body></html>

There's also a function available to do this for the currently needed
resources::

  >>> print resource.render_topbottom_into_html(html)
  <html><head>
      <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  rest of head</head><body>rest of body<script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/y2.js"></script></body></html>

Using WSGI middleware to insert into HTML
=========================================

There is also a WSGI middleware available to insert the top (and bottom)
into the HTML. We are using WebOb to create a response object that will
serve as our WSGI application.

We create a simple WSGI application. In our application we declare that
we need a resource (``y1``) and put that in the WSGI ``environ`` under the
key ``hurry.resource.needed``::
 
  >>> def app(environ, start_response):
  ...    start_response('200 OK', [])
  ...    needed = environ['hurry.resource.needed'] = NeededInclusions()
  ...    needed.need(y1)
  ...    return ['<html><head></head><body</body></html>']

We now wrap this in our middleware, so that the middleware is activated::

  >>> from hurry.resource.wsgi import Middleware
  >>> wrapped_app = Middleware(app)

Now we make a request (using webob for convenience)::

  >>> import webob
  >>> req = webob.Request.blank('/')
  >>> res = req.get_response(wrapped_app) 

We can now see that the resources are added to the HTML by the middleware::

  >>> print res.body
  <html><head>
      <link rel="stylesheet" type="text/css" href="http://localhost/static/foo/b.css" />
  <script type="text/javascript" src="http://localhost/static/foo/a.js"></script>
  <script type="text/javascript" src="http://localhost/static/foo/c.js"></script>
  </head><body</body></html>

When we set the response Content-Type to non-HTML, the middleware
won't be active even if we need things and the body appears to contain
HTML::

  >>> def app(environ, start_response):
  ...    start_response('200 OK', [('Content-Type', 'text/plain')])
  ...    needed = environ['hurry.resource.needed'] = NeededInclusions()
  ...    needed.need(y1)
  ...    return ['<html><head></head><body</body></html>']
  >>> wrapped_app = Middleware(app)
  >>> req = webob.Request.blank('/')
  >>> res = req.get_response(wrapped_app)
  >>> res.body
  '<html><head></head><body</body></html>'

bottom convenience
==================

Like for ``need`` and ``mode``, there is also a convenience spelling for
``bottom``::

  >>> request = Request()
  >>> l1 = ResourceInclusion(foo, 'l1.js', bottom=True)
  >>> l1.need()

Let's look at the resources needed by default::

  >>> c = component.getUtility(ICurrentNeededInclusions)
  >>> top, bottom = c().render_topbottom()
  >>> print top
  <script type="text/javascript" src="http://localhost/static/foo/l1.js"></script>
  >>> print bottom
  <BLANKLINE>

Let's now change the bottom mode using the convenience
``hurry.resource.bottom`` spelling::

  >>> from hurry.resource import bottom
  >>> bottom()

Re-rendering will show it's honoring the bottom setting::

  >>> top, bottom = c().render_topbottom()
  >>> print top
  <BLANKLINE>
  >>> print bottom
  <script type="text/javascript" src="http://localhost/static/foo/l1.js"></script>

Generating resource code
========================

Sometimes it is useful to generate code that expresses a complex
resource dependency structure. One example of that is in
``hurry.yui``. We can use the ``generate_code`` function to render resource
inclusions::

  >>> i1 = ResourceInclusion(foo, 'i1.js')
  >>> i2 = ResourceInclusion(foo, 'i2.js', depends=[i1])
  >>> i3 = ResourceInclusion(foo, 'i3.js', depends=[i2])
  >>> i4 = ResourceInclusion(foo, 'i4.js', depends=[i1])
  >>> i5 = ResourceInclusion(foo, 'i5.js', depends=[i4, i3])

  >>> from hurry.resource import generate_code
  >>> print generate_code(i1=i1, i2=i2, i3=i3, i4=i4, i5=i5)
  from hurry.resource import Library, ResourceInclusion
  <BLANKLINE>
  foo = Library('foo')
  <BLANKLINE>
  i1 = ResourceInclusion(foo, 'i1.js')
  i2 = ResourceInclusion(foo, 'i2.js', depends=[i1])
  i3 = ResourceInclusion(foo, 'i3.js', depends=[i2])
  i4 = ResourceInclusion(foo, 'i4.js', depends=[i1])
  i5 = ResourceInclusion(foo, 'i5.js', depends=[i4, i3])

Let's look at a more complicated example with modes and superseders::

  >>> j1 = ResourceInclusion(foo, 'j1.js', debug='j1-debug.js')
  >>> j2 = ResourceInclusion(foo, 'j2.js', debug='j2-debug.js')
  >>> giantj = ResourceInclusion(foo, 'giantj.js', supersedes=[j1, j2],
  ...                            debug='giantj-debug.js')

  >>> print generate_code(j1=j1, j2=j2, giantj=giantj)
  from hurry.resource import Library, ResourceInclusion
  <BLANKLINE>
  foo = Library('foo')
  <BLANKLINE>
  j1 = ResourceInclusion(foo, 'j1.js', debug='j1-debug.js')
  j2 = ResourceInclusion(foo, 'j2.js', debug='j2-debug.js')
  giantj = ResourceInclusion(foo, 'giantj.js', supersedes=[j1, j2], debug='giantj-debug.js')

We can control the name the inclusion will get in the source code by
using keyword parameters::

  >>> print generate_code(hoi=i1)
  from hurry.resource import Library, ResourceInclusion
  <BLANKLINE>
  foo = Library('foo')
  <BLANKLINE>
  hoi = ResourceInclusion(foo, 'i1.js')

  >>> print generate_code(hoi=i1, i2=i2)
  from hurry.resource import Library, ResourceInclusion
  <BLANKLINE>
  foo = Library('foo')
  <BLANKLINE>
  hoi = ResourceInclusion(foo, 'i1.js')
  i2 = ResourceInclusion(foo, 'i2.js', depends=[hoi])

Sorting inclusions by dependency
================================

This is more a footnote than something that you should be concerned
about. In case assumptions in this library are wrong or there are
other reasons you would like to sort resource inclusions that come in
some arbitrary order into one where the dependency relation makes
sense, you can use ``sort_inclusions_topological``::

  >>> from hurry.resource import sort_inclusions_topological

Let's make a list of resource inclusions not sorted by dependency::

  >>> i = [a5, a3, a1, a2, a4]
  >>> sort_inclusions_topological(i)
  [<ResourceInclusion 'a1.js' in library 'foo'>, 
   <ResourceInclusion 'a4.js' in library 'foo'>, 
   <ResourceInclusion 'a2.js' in library 'foo'>, 
   <ResourceInclusion 'a3.js' in library 'foo'>, 
   <ResourceInclusion 'a5.js' in library 'foo'>]


Inclusion renderers
===================

The HTML fragments for inclusions are rendered by ``inclusion renderers``
that are simple functions registered per extension.

Renderers are registered in the ``inclusion_renderers`` dictionary:

  >>> from hurry.resource.core import inclusion_renderers
  >>> sorted(inclusion_renderers)
  ['.css', '.js', '.kss']

Renderers render HTML fragments using given resource URL:

  >>> inclusion_renderers['.js']('http://localhost/script.js')
  '<script type="text/javascript" src="http://localhost/script.js"></script>'

Let's create an inclusion of unknown resource:

  >>> a6 = ResourceInclusion(foo, 'nothing.unknown')

  >>> from hurry.resource.core import render_inclusions
  >>> render_inclusions([a6])
  Traceback (most recent call last):
  ...
  UnknownResourceExtension: Unknown resource extension .unknown for resource
                            inclusion: <ResourceInclusion 'nothing.unknown'
                            in library 'foo'>

Now let's add a renderer for our ".unknown" extension and try again:

  >>> def render_unknown(url):
  ...     return '<link rel="unknown" href="%s" />' % url
  >>> inclusion_renderers['.unknown'] = render_unknown

  >>> render_inclusions([a6])
  '<link rel="unknown" href="http://localhost/static/foo/nothing.unknown" />'
