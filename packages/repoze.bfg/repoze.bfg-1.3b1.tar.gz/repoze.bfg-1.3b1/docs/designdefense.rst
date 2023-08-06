.. _design_defense:

Defending BFG's Design
======================

From time to time, challenges to various aspects of :mod:`repoze.bfg`
design are lodged.  To give context to discussions that follow, we
detail some of the design decisions and trade-offs here.  In some
cases, we acknowledge that the framework can be made better and we
describe future steps which will be taken to improve it; in some cases
we just file the challenge as "noted", as obviously you can't please
everyone all of the time.

BFG Uses A Zope Component Architecture ("ZCA") Registry
-------------------------------------------------------

:mod:`repoze.bfg` uses a :term:`Zope Component Architecture` (ZCA)
"component registry" as its :term:`application registry` under the
hood.  This is a point of some contention.  :mod:`repoze.bfg` is of a
:term:`Zope` pedigree, so it was natural for its developers to use a
ZCA registry at its inception.  However, we understand that using a
ZCA registry has issues and consequences, which we've attempted to
address as best we can.  Here's an introspection about
:mod:`repoze.bfg` use of a ZCA registry, and the trade-offs its usage
involves.

Problems
++++++++

The "global" API that may be used to access data in a ZCA "component
registry" is not particularly pretty or intuitive, and sometimes it's
just plain obtuse.  Likewise, the conceptual load on a casual source
code reader of code that uses the ZCA global API is somewhat high.
Consider a ZCA neophyte reading the code that performs a typical
"unnamed utility" lookup using the :func:`zope.component.getUtility`
global API:

.. ignore-next-block
.. code-block:: python
   :linenos:

   from repoze.bfg.interfaces import ISettings
   from zope.component import getUtility
   settings = getUtility(ISettings)

After this code runs, ``settings`` will be a Python dictionary.  But
it's unlikely that any "civilian" would know that just by reading the
code.  There are a number of comprehension issues with the bit of code
above that are obvious.

First, what's a "utility"?  Well, for the purposes of this discussion,
and for the purpose of the code above, it's just not very important.
If you really want to know, you can read `this
<http://www.muthukadan.net/docs/zca.html#utility>`_.  However, still,
readers of such code need to understand the concept in order to parse
it.  This is problem number one.

Second, what's this ``ISettings`` thing?  It's an :term:`interface`.
Is that important here?  Not really, we're just using it as a "key"
for some lookup based on its identity as a marker: it represents an
object that has the dictionary API, but that's not very important in
this context.  That's problem number two.

Third of all, what does the ``getUtility`` function do?  It's
performing a lookup for the ``ISettings`` "utility" that should
return.. well, a utility.  Note how we've already built up a
dependency on the understanding of an :term:`interface` and the
concept of "utility" to answer this question: a bad sign so far.  Note
also that the answer is circular, a *really* bad sign.

Fourth, where does ``getUtility`` look to get the data?  Well, the
"component registry" of course.  What's a component registry?  Problem
number four.

Fifth, assuming you buy that there's some magical registry hanging
around, where *is* this registry?  *Homina homina*... "around"?
That's sort of the best answer in this context (a more specific answer
would require knowledge of internals).  Can there be more than one
registry?  Yes.  So *which* registry does it find the registration in?
Well, the "current" registry of course.  In terms of
:mod:`repoze.bfg`, the current registry is a thread local variable.
Using an API that consults a thread local makes understanding how it
works non-local.

You've now bought in to the fact that there's a registry that is just
"hanging around".  But how does the registry get populated?  Why,
:term:`ZCML` of course.  Sometimes.  Or via imperative code.  In this
particular case, however, the registration of ``ISettings`` is made by
the framework itself "under the hood": it's not present in any ZCML
nor was it performed imperatively.  This is extremely hard to
comprehend.  Problem number six.

Clearly there's some amount of cognitive load here that needs to be
borne by a reader of code that extends the :mod:`repoze.bfg` framework
due to its use of the ZCA, even if he or she is already an expert
Python programmer and whom is an expert in the domain of web
applications.  This is suboptimal.

Ameliorations
+++++++++++++

First, the primary amelioration: :mod:`repoze.bfg` *does not expect
application developers to understand ZCA concepts or any of its APIs*.
If an *application* developer needs to understand a ZCA concept or API
during the creation of a :mod:`repoze.bfg` application, we've failed
on some axis.

Instead, the framework hides the presence of the ZCA registry behind
special-purpose API functions that *do* use ZCA APIs.  Take for
example the ``repoze.bfg.security.authenticated_userid`` function,
which returns the userid present in the current request or ``None`` if
no userid is present in the current request.  The application
developer calls it like so:

.. ignore-next-block
.. code-block:: python
   :linenos:

   from repoze.bfg.security import authenticated_userid
   userid = authenticated_userid(request)

He now has the current user id.

Under its hood however, the implementation of ``authenticated_userid``
is this:

.. code-block:: python
   :linenos:

   def authenticated_userid(request):
       """ Return the userid of the currently authenticated user or
       ``None`` if there is no authentication policy in effect or there
       is no currently authenticated user. """

       registry = request.registry # the ZCA component registry
       policy = registry.queryUtility(IAuthenticationPolicy)
       if policy is None:
           return None
       return policy.authenticated_userid(request)

Using such wrappers, we strive to always hide the ZCA API from
application developers.  Application developers should just never know
about the ZCA API: they should call a Python function with some object
germane to the domain as an argument, and it should returns a result.
A corollary that follows is that any reader of an application that has
been written using :mod:`repoze.bfg` needn't understand the ZCA API
either.

Hiding the ZCA API from application developers and code readers is a
form of enhancing "domain specificity".  No application developer
wants to need to understand the minutiae of the mechanics of how a web
framework does its thing.  People want to deal in concepts that are
closer to the domain they're working in: for example, web developers
want to know about *users*, not *utilities*.  :mod:`repoze.bfg` uses
the ZCA as an implementation detail, not as a feature which is exposed
to end users.

However, unlike application developers, *framework developers*,
including people who want to override :mod:`repoze.bfg` functionality
via preordained framework plugpoints like traversal or view lookup
*must* understand the ZCA registry API.

:mod:`repoze.bfg` framework developers were so concerned about
conceptual load issues of the ZCA registry API for framework
developers that a `replacement registry implementation
<http://svn.repoze.org/repoze.component/trunk>`_ named
:mod:`repoze.component` was actually developed.  Though this package
has a registry implementation which is fully functional and
well-tested, and its API is much nicer than the ZCA registry API, work
on it was largely abandoned and it is not used in :mod:`repoze.bfg`.
We continued to use a ZCA registry within :mod:`repoze.bfg` because it
ultimately proved a better fit.

.. note:: We continued using ZCA registry rather than disusing it in
   favor of using the registry implementation in
   :mod:`repoze.component` largely because the ZCA concept of
   interfaces provides for use of an interface hierarchy, which is
   useful in a lot of scenarios (such as context type inheritance).
   Coming up with a marker type that was something like an interface
   that allowed for this functionality seemed like it was just
   reinventing the wheel.

Making framework developers and extenders understand the ZCA registry
API is a trade-off.  We (the :mod:`repoze.bfg` developers) like the
features that the ZCA registry gives us, and we have long-ago borne
the weight of understanding what it does and how it works.  The
authors of :mod:`repoze.bfg` understand the ZCA deeply and can read
code that uses it as easily as any other code.

But we recognize that developers who my want to extend the framework
are not as comfortable with the ZCA registry API as the original
developers are with it.  So, for the purposes of being kind to
third-party :mod:`repoze.bfg` framework developers in, we've drawn
some lines in the sand.

#) In all "core" code, We've made use of ZCA global API functions such
   as ``zope.component.getUtility`` and ``zope.component.getAdapter``
   the exception instead of the rule.  So instead of:

   .. code-block:: python
      :linenos:

      from repoze.bfg.interfaces import IAuthenticationPolicy
      from zope.component import getUtility
      policy = getUtility(IAuthenticationPolicy)

   :mod:`repoze.bfg` code will usually do:

   .. code-block:: python
      :linenos:

      from repoze.bfg.interfaces import IAuthenticationPolicy
      from repoze.bfg.threadlocal import get_current_registry
      registry = get_current_registry()
      policy = registry.getUtility(IAuthenticationPolicy)

   While the latter is more verbose, it also arguably makes it more
   obvious what's going on.  All of the :mod:`repoze.bfg` core code uses
   this pattern rather than the ZCA global API.

#) We've turned the component registry used by :mod:`repoze.bfg` into
   something that is accessible using the plain old dictionary API
   (like the :mod:`repoze.component` API).  For example, the snippet
   of code in the problem section above was:

   .. code-block:: python
      :linenos:

      from repoze.bfg.interfaces import ISettings
      from zope.component import getUtility
      settings = getUtility(ISettings)

   In a better world, we might be able to spell this as:

   .. code-block:: python
      :linenos:

      from repoze.bfg.threadlocal import get_current_registry

      registry = get_current_registry()
      settings = registry['settings']

   In this world, we've removed the need to understand utilities and
   interfaces, because we've disused them in favor of a plain dictionary
   lookup.  We *haven't* removed the need to understand the concept of a
   *registry*, but for the purposes of this example, it's simply a
   dictionary.  We haven't killed off the concept of a thread local
   either.  Let's kill off thread locals, pretending to want to do this
   in some code that has access to the :term:`request`:

   .. code-block:: python
      :linenos:

      registry = request.registry
      settings = registry['settings']

   In *this* world, we've reduced the conceptual problem to understanding
   attributes and the dictionary API.  Every Python programmer knows
   these things, even framework programmers.

While :mod:`repoze.bfg` still uses some suboptimal unnamed utility
registrations, future versions of it will where possible disuse these
things in favor of straight dictionary assignments and lookups, as
demonstrated above, to be kinder to new framework developers.  We'll
continue to seek ways to reduce framework developer cognitive load.

Rationale
+++++++++

Here are the main rationales involved in the :mod:`repoze.bfg`
decision to use the ZCA registry:

- Pedigree.  A nontrivial part of the answer to this question is
  "pedigree".  Much of the design of :mod:`repoze.bfg` is stolen
  directly from :term:`Zope`.  Zope uses the ZCA registry to do a
  number of tricks.  :mod:`repoze.bfg` mimics these tricks, and,
  because the ZCA registry works well for that set of tricks,
  :mod:`repoze.bfg` uses it for the same purposes.  For example, the
  way that :mod:`repoze.bfg` maps a :term:`request` to a :term:`view
  callable` is lifted almost entirely from Zope.  The ZCA registry
  plays an important role in the particulars of how this request to
  view mapping is done.

- Features.  The ZCA component registry essentially provides what can
  be considered something like a "superdictionary", which allows for
  more complex lookups than retrieving a value based on a single key.
  Some of this lookup capability is very useful for end users, such as
  being able to register a view that is only found when the context is
  some class of object, or when the context implements some
  :term:`interface`.

- Singularity.  There's only one "place" where "application
  configuration" lives in a :mod:`repoze.bfg` application: in a
  component registry.  The component registry answers questions made
  to it by the framework at runtime based on the configuration of *an
  application*.  Note: "an application" is not the same as "a
  process", multiple independently configured copies of the same
  :mod:`repoze.bfg` application are capable of running in the same
  process space.

- Composability.  A ZCA component registry can be populated
  imperatively, or there's an existing mechanism to populate a
  registry via the use of a configuration file (ZCML).  We didn't need
  to write a frontend from scratch to make use of
  configuration-file-driven registry population.

- Pluggability.  Use of the ZCA registry allows for framework
  extensibility via a well-defined and widely understood plugin
  architecture.  As long as framework developers and extenders
  understand the ZCA registry, it's possible to extend
  :mod:`repoze.bfg` almost arbitrarily.  For example, it's relatively
  easy to build a ZCML directive that registers several views "all at
  once", allowing app developers to use that ZCML directive as a
  "macro" in code that they write.  This is somewhat of a
  differentiating feature from other (non-Zope) frameworks.

- Testability.  Judicious use of the ZCA registry in framework code
  makes testing that code slightly easier.  Instead of using
  monkeypatching or other facilities to register mock objects for
  testing, we inject dependencies via ZCA registrations and then use
  lookups in the code find our mock objects.

- Speed.  The ZCA registry is very fast for a specific set of complex
  lookup scenarios that :mod:`repoze.bfg` uses, having been optimized
  through the years for just these purposes.  The ZCA registry
  contains optional C code for this purpose which demonstrably has no
  (or very few) bugs.

- Ecosystem.  Many existing Zope packages can be used in
  :mod:`repoze.bfg` with few (or no) changes due to our use of the ZCA
  registry and :term:`ZCML`.

Conclusion
++++++++++

If you only *develop applications* using :mod:`repoze.bfg`, there's
not much to complain about here.  You just should never need to
understand the ZCA registry or even know about its presence: use
documented :mod:`repoze.bfg` APIs instead.  However, you may be an
application developer who doesn't read API documentation because it's
unmanly. Instead you read the raw source code, and because you haven't
read the documentation, you don't know what functions, classes, and
methods even *form* the :mod:`repoze.bfg` API.  As a result, you've
now written code that uses internals and you've pained yourself into a
conceptual corner as a result of needing to wrestle with some
ZCA-using implementation detail.  If this is you, it's extremely hard
to have a lot of sympathy for you.  You'll either need to get familiar
with how we're using the ZCA registry or you'll need to use only the
documented APIs; that's why we document them as APIs.

If you *extend* or *develop* :mod:`repoze.bfg` (create new ZCML
directives, use some of the more obscure "ZCML hooks" as described in
:ref:`hooks_chapter`, or work on the :mod:`repoze.bfg` core code), you
will be faced with needing to understand at least some ZCA concepts.
The ZCA registry API is quirky: we've tried to make it at least
slightly nicer by disusing it for common registrations and lookups
such as unnamed utilities.  Some places it's used unabashedly, and
will be forever.  We know it's quirky, but it's also useful and
fundamentally understandable if you take the time to do some reading
about it.

BFG Uses Interfaces Too Liberally
---------------------------------

In this `TOPP Engineering blog entry
<http://www.coactivate.org/projects/topp-engineering/blog/2008/10/20/what-bothers-me-about-the-component-architecture/>`_,
Ian Bicking asserts that the way :mod:`repoze.bfg` uses a Zope
interface to represent an HTTP request method adds too much
indirection for not enough gain.  We agreed in general, and for this
reason, :mod:`repoze.bfg` version 1.1 added :term:`view predicate` and
:term:`route predicate` modifiers to view configuration.  Predicates
are request-specific (or :term:`context` -specific) matching narrowers
which don't use interfaces.  Instead, each predicate uses a
domain-specific string as a match value.

For example, to write a view configuration which matches only requests
with the ``POST`` HTTP request method, you might write a ``@bfg_view``
decorator which mentioned the ``request_method`` predicate:

.. code-block:: python
   :linenos:

   from repoze.bfg.view import bfg_view
   @bfg_view(name='post_view', request_method='POST', renderer='json')
   def post_view(request):
       return 'POSTed'

You might further narrow the matching scenario by adding an ``accept``
predicate that narrows matching to something that accepts a JSON
response:

.. code-block:: python
   :linenos:

   from repoze.bfg.view import bfg_view
   @bfg_view(name='post_view', request_method='POST', accept='application/json',
             renderer='json')
   def post_view(request):
       return 'POSTed'

Such a view would only match when the request indicated that HTTP
request method was ``POST`` and that the remote user agent passed
``application/json`` (or, for that matter, ``application/*``) in its
``Accept`` request header.

"Under the hood", these features make no use of interfaces.

For more information about predicates, see
:ref:`view_predicates_in_1dot1` and :ref:`route_predicates_in_1dot1`.

Many "prebaked" predicates exist.  However, use of only "prebaked"
predicates, however, doesn't entirely meet Ian's criterion.  He would
like to be able to match a request using a lambda or another function
which interrogates the request imperatively.  In version 1.2, we
acommodate this by allowing people to define "custom" view predicates:

.. code-block:: python
   :linenos:

   from repoze.bfg.view import bfg_view
   from webob import Response

   def subpath(context, request):
       return request.subpath and request.subpath[0] == 'abc'

   @bfg_view(custom_predicates=(subpath,))
   def aview(request):
       return Response('OK')

The above view will only match when the first element of the request's
:term:`subpath` is ``abc``.

.. _zcml_encouragement:

BFG "Encourages Use of ZCML"
----------------------------

:term:`ZCML` is a configuration language that can be used to configure
the :term:`Zope Component Architecture` registry that
:mod:`repoze.bfg` uses as its application configuration.

Quick answer: well, it doesn't *really* encourage the use of ZCML.  In
:mod:`repoze.bfg` 1.0 and 1.1, application developers could use
decorators for the most common form of configuration.  But, yes, a
:mod:`repoze.bfg` 1.0/1.1 application needed to possess a ZCML file
for it to begin executing successfully even if its only contents were
a ``<scan>`` directive that kicked off a scan to find decorated view
callables.

In the interest of completeness and in the spirit of providing a
lowest common denominator, :mod:`repoze.bfg` 1.2 includes a completely
imperative mode for all configuration.  You will be able to make
"single file" apps in this mode, which should help people who need to
see everything done completely imperatively.  For example, the very
most basic :mod:`repoze.bfg` "helloworld" program has become
something like:

.. code-block:: python
   :linenos:

   from webob import Response
   from paste.httpserver import serve
   from repoze.bfg.configuration import Configurator

   def hello_world(request):
       return Response('Hello world!')

   if __name__ == '__main__':
       config = Configurator()
       config.begin()
       config.add_view(hello_world)
       config.end()
       app = config.make_wsgi_app()
       serve(app)

In this mode, no ZCML is required for end users.  Hopefully this mode
will allow people who are used to doing everything imperatively feel
more comfortable.

BFG Uses ZCML; ZCML is XML and I Don't Like XML
-----------------------------------------------

:term:`ZCML` is a configuration language in the XML syntax.  Due to
the "imperative configuration" feature (new in :mod:`repoze.bfg` 1.2),
you don't need to use ZCML at all if you start a project from scratch.
But if you really do want to perform declarative configuration,
perhaps because you want to build an extensible application, you will
need to use and understand it.

:term:`ZCML` contains elements that are mostly singleton tags that are
called *declarations*.  For an example:

.. code-block:: xml
   :linenos:

   <route
      view=".views.my_view"
      path="/"
      name="root"
      />

This declaration associates a :term:`view` with a route pattern. 

All :mod:`repoze.bfg` declarations are singleton tags, unlike many
other XML configuration systems.  No XML *values* in ZCML are
meaningful; it's always just XML tags and attributes.  So in the very
common case it's not really very much different than an otherwise
"flat" configuration format like ``.ini``, except a developer can
*create* a directive that requires nesting (none of these exist in
:mod:`repoze.bfg` itself), and multiple "sections" can exist with the
same "name" (e.g. two ``<route>`` declarations) must be able to exist
simultaneously.

You might think some other configuration file format would be better.
But all configuration formats suck in one way or another.  I
personally don't think any of our lives would be markedly better if
the declarative configuration format used by :mod:`repoze.bfg` were
YAML, JSON, or INI.  It's all just plumbing that you mostly cut and
paste once you've progressed 30 minutes into your first project.
Folks who tend to agitate for another configuration file format are
folks that haven't yet spent that 30 minutes.

.. _model_traversal_confusion:

BFG Uses "Model" To Represent A Node In The Graph of Objects Traversed
----------------------------------------------------------------------

The :mod:`repoze.bfg` documentation refers to the graph being
traversed when :term:`traversal` is used as a "model graph".  Some of
the :mod:`repoze.bfg` APIs also use the word "model" in them when
referring to a node in this graph (e.g. ``repoze.bfg.url.model_url``).

A terminology overlap confuses people who write applications that
always use ORM packages such as SQLAlchemy, which has a different
notion of the definition of a "model".  When using the API of common
ORM packages, its conception of "model" is almost certainly not a
directed acyclic graph (as may be the case in many graph databases).
Often model objects must be explicitly manufactured by an ORM as a
result of some query performed by a :term:`view`.  As a result, it can
be unnatural to think of the nodes traversed as "model" objects if you
develop your application using traversal and a relational database.
When you develop such applications, the things that :mod:`repoze.bfg`
refers to as "models" in such an application may just be stand-ins
that perform a query and generate some wrapper *for* an ORM "model"
(or set of ORM models).  The graph *might* be composed completely of
"model" objects (as defined by the ORM) but it also might not be.

The naming impedance mismatch between the way the term "model" is used
to refer to a node in a graph in :mod:`repoze.bfg` and the way the
term "model" is used by packages like SQLAlchemy is unfortunate.  For
the purpose of avoiding confusion, if we had it to do all over again,
we might refer to the graph that :mod:`repoze.bfg` traverses a "node
graph" or "object graph" rather than a "model graph", but since we've
baked the name into the API, it's a little late.  Sorry.

In our defense, many :mod:`repoze.bfg` applications (especially ones
which use :term:`ZODB`) do indeed traverse a graph full of model
nodes.  Each node in the graph is a separate persistent object that is
stored within a database.  This was the use case considered when
coming up with the "model" terminology.

I Can't Figure Out How "BFG" Is Related to "Repoze"
---------------------------------------------------

When the `Repoze project <http://repoze.org>`_ was first started,
:mod:`repoze.bfg` did not exist.  The `website <http://repoze.org>`_
for the project had (and still has, of this writing) a tag line of
"Plumbing Zope into the WSGI Pipeline", and contained descriptions of
:term:`WSGI` middleware that were inspired by Zope features, and
applications that help :term:`Zope` to run within a WSGI environment.
The original intent was to create a "namespace" of packages
("repoze.*") that contained software that formed a decomposition of
Zope features into more WSGI-friendly components.  It was never the
intention of the Repoze project to actually create another web
framework.

However, as time progressed, the folks who ran the Repoze project
decided to create :mod:`repoze.bfg`, which *is* a web framework.  Due
to an early naming mistake, the software composing the framework was
named :mod:`repoze.bfg`.  This mistake was not corrected before the
software garnered a significant user base, and in the interest of
backwards compatibility, most likely never will be.  While
:mod:`repoze.bfg` uses Zope technology, it is otherwise unrelated to
the original goals of "Repoze" as stated on the repoze.org website.
If we had it to do all over again, the :mod:`repoze.bfg` package would
be named simply :mod:`bfg`.  But we don't have it to do all over
again.

At this point, therefore, the name "Repoze" should be considered
basically just a "brand".  Its presence in the name of a package means
nothing except that it has an origin as a piece of software developed
by a member of the Repoze community.

BFG Does Traversal, And I Don't Like Traversal
----------------------------------------------

In :mod:`repoze.bfg`, :term:`traversal` is the act of resolving a URL
path to a :term:`model` object in an object graph.  Some people are
uncomfortable with this notion, and believe it is wrong.

This is understandable.  The people who believe it is wrong almost
invariably have all of their data in a relational database.
Relational databases aren't naturally hierarchical, so "traversing"
one like a graph is not possible.  This problem is related to
:ref:`model_traversal_confusion`.

Folks who deem traversal unilaterally "wrong" are neglecting to take
into account that many persistence mechanisms *are* hierarchical.
Examples include a filesystem, an LDAP database, a :term:`ZODB` (or
another type of graph) database, an XML document, and the Python
module namespace.  It is often convenient to model the frontend to a
hierarchical data store as a graph, using traversal to apply views to
objects that either *are* the nodes in the graph being traversed (such
as in the case of ZODB) or at least ones which stand in for them (such
as in the case of wrappers for files from the filesystem).

Also, many website structures are naturally hierarchical, even if the
data which drives them isn't.  For example, newspaper websites are
often extremely hierarchical: sections within sections within
sections, ad infinitum.  If you want your URLs to indicate this
structure, and the structure is indefinite (the number of nested
sections can be "N" instead of some fixed number), traversal is an
excellent way to model this, even if the backend is a relational
database.  In this situation, the graph being traversed is actually
less a "model graph" than a site structure.

But the point is ultimately moot.  If you use :mod:`repoze.bfg`, and
you don't want to model your application in terms of traversal, you
needn't use it at all.  Instead, use :term:`URL dispatch` to map URL
paths to views.

BFG Does URL Dispatch, And I Don't Like URL Dispatch
----------------------------------------------------

In :mod:`repoze.bfg`, :term:`url dispatch` is the act of resolving a
URL path to a :term:`view` callable by performing pattern matching
against some set of ordered route definitions.  The route definitions
are examined in order: the first pattern which matches is used to
associate the URL with a view callable.

Some people are uncomfortable with this notion, and believe it is
wrong.  These are usually people who are steeped deeply in
:term:`Zope`.  Zope does not provide any mechanism except
:term:`traversal` to map code to URLs.  This is mainly because Zope
effectively requires use of :term:`ZODB`, which is a hierarchical
object store.  Zope also supports relational databases, but typically
the code that calls into the database lives somewhere in the ZODB
object graph (or at least is a :term:`view` related to a node in the
object graph), and traversal is required to reach this code.

I'll argue that URL dispatch is ultimately useful, even if you want to
use traversal as well.  You can actually *combine* URL dispatch and
traversal in :mod:`repoze.bfg` (see :ref:`hybrid_chapter`).  One
example of such a usage: if you want to emulate something like Zope
2's "Zope Management Interface" UI on top of your object graph (or any
administrative interface), you can register a route like ``<route
name="manage" path="manage/*traverse"/>`` and then associate
"management" views in your code by using the ``route_name`` argument
to a ``view`` configuration, e.g. ``<view view=".some.callable"
context=".some.Model" route_name="manage"/>``.  If you wire things up
this way someone then walks up to for example, ``/manage/ob1/ob2``,
they might be presented with a management interface, but walking up to
``/ob1/ob2`` would present them with the default object view.  There
are other tricks you can pull in these hybrid configurations if you're
clever (and maybe masochistic) too.

Also, if you are a URL dispatch hater, if you should ever be asked to
write an application that must use some legacy relational database
structure, you might find that using URL dispatch comes in handy for
one-off associations between views and URL paths.  Sometimes it's just
pointless to add a node to the object graph that effectively
represents the entry point for some bit of code.  You can just use a
route and be done with it.  If a route matches, a view associated with
the route will be called; if no route matches, :mod:`repoze.bfg` falls
back to using traversal.

But the point is ultimately moot.  If you use :mod:`repoze.bfg`, and
you really don't want to use URL dispatch, you needn't use it at all.
Instead, use :term:`traversal` exclusively to map URL paths to views,
just like you do in :term:`Zope`.

BFG Views Do Not Accept Arbitrary Keyword Arguments
---------------------------------------------------

Many web frameworks (Zope, TurboGears, Pylons, Django) allow for their
variant of a :term:`view callable` to accept arbitrary keyword or
positional arguments, which are "filled in" using values present in
the ``request.POST`` or ``request.GET`` dictionaries or by values
present in the "route match dictionary".  For example, a Django view
will accept positional arguments which match information in an
associated "urlconf" such as ``r'^polls/(?P<poll_id>\d+)/$``:

.. code-block:: python
   :linenos:

   def aview(request, poll_id):
       return HttpResponse(poll_id)

Zope, likewise allows you to add arbitrary keyword and positional
arguments to any method of a model object found via traversal:

.. ignore-next-block
.. code-block:: python
   :linenos:

   from persistent import Persistent

   class MyZopeObject(Persistent):
        def aview(self, a, b, c=None):
            return '%s %s %c' % (a, b, c)

When this method is called as the result of being the published
callable, the Zope request object's GET and POST namespaces are
searched for keys which match the names of the positional and keyword
arguments in the request, and the method is called (if possible) with
its argument list filled with values mentioned therein.  TurboGears
and Pylons operate similarly.

:mod:`repoze.bfg` has neither of these features.  :mod:`repoze.bfg`
view callables always accept only ``context`` and ``request`` (or just
``request``), and no other arguments.  The rationale: this argument
specification matching done aggressively can be costly, and
:mod:`repoze.bfg` has performance as one of its main goals, so we've
decided to make people obtain information by interrogating the request
object for it in the view body instead of providing magic to do
unpacking into the view argument list.  The feature itself also just
seems a bit like a gimmick.  Getting the arguments you want explicitly
from the request via getitem is not really very hard; it's certainly
never a bottleneck for the author when he writes web apps.

It is possible to replicate the Zope-like behavior in a view callable
decorator, however, should you badly want something like it back.  No
such decorator currently exists.  If you'd like to create one, Google
for "zope mapply" and adapt the function you'll find to a decorator
that pulls the argument mapping information out of the
``request.params`` dictionary.

A similar feature could be implemented to provide the Django-like
behavior as a decorator by wrapping the view with a decorator that
looks in ``request.matchdict``.

It's possible at some point that :mod:`repoze.bfg` will grow some form
of argument matching feature (it would be simple to make it an
always-on optional feature that has no cost unless you actually use
it) for, but currently it has none.

BFG Provides Too Few "Rails"
----------------------------

By design, :mod:`repoze.bfg` is not a particularly "opinionated" web
framework.  It has a relatively parsimonious feature set.  It contains
no built in ORM nor any particular database bindings.  It contains no
form generation framework.  It does not contain a sessioning library.
It has no administrative web user interface.  It has no built in text
indexing.  It does not dictate how you arrange your code.

Such opinionated functionality exists in applications and frameworks
built *on top* of :mod:`repoze.bfg`.  It's intended that higher-level
systems emerge built using :mod:`repoze.bfg` as a base.  See also
:ref:`apps_are_extensible`.

BFG Provides Too Many "Rails"
-----------------------------

:mod:`repoze.bfg` provides some features that other web frameworks do
not.  Most notably it has machinery which resolves a URL first to a
:term:`context` before calling a view (which has the capability to
accept the context in its argument list), and a declarative
authorization system that makes use of this feature.  Most other web
frameworks besides :term:`Zope`, from which the pattern was stolen,
have no equivalent core feature.

We consider this an important feature for a particular class of
applications (CMS-style applications, which the authors are often
commissioned to write) that usually use :term:`traversal` against a
persistent object graph.  The object graph contains security
declarations as :term:`ACL` objects.

Having context-sensitive declarative security for individual objects
in the object graph is simply required for this class of application.
Other frameworks save for Zope just do not have this feature.  This is
one of the primary reasons that :mod:`repoze.bfg` was actually
written.

If you don't like this, it doesn't mean you can't use
:mod:`repoze.bfg`.  Just ignore this feature and avoid configuring an
authorization or authentication policy and using ACLs.  You can build
"Pylons-style" applications using :mod:`repoze.bfg` that use their own
security model via decorators or plain-old-imperative logic in view
code.

BFG Is Too Big
--------------

"The :mod:`repoze.bfg` compressed tarball is 1MB.  It must be
enormous!"

No.  We just ship it with test code and helper templates.  Here's a
breakdown of what's included in subdirectories of the package tree:

docs/

  2.2MB

repoze/bfg/tests

  580KB

repoze/bfg/paster_templates

  372KB

repoze/bfg (except for ``repoze/bfg/tests and repoze/bfg/paster_templates``)

  316K

The actual :mod:`repoze.bfg` runtime code is about 10% of the total
size of the tarball omitting docs, helper templates used for package
generation, and test code.  Of the approximately 13K lines of Python
code in the package, the code that actually has a chance of executing
during normal operation, excluding tests and paster template Python
files, accounts for approximately 3K lines of Python code.  This is
comparable to Pylons, which ships with a little over 2K lines of
Python code, excluding tests.

BFG Has Too Many Dependencies
-----------------------------

This is true.  At the time of this writing, the total number of Python
package distributions that :mod:`repoze.bfg` depends upon transitively
is 14 if you use Python 2.6 or 2.7, or 16 if you use Python 2.4 or
2.5.  This is a lot more than zero package distribution dependencies:
a metric which various Python microframeworks and Django boast.

The :mod:`zope.component` and :mod:`zope.configuration` packages on
which :mod:`repoze.bfg` depends have transitive dependencies on
several other packages (:mod:`zope.schema`, :mod:`zope.i18n`,
:mod:`zope.event`, :mod:`zope.interface`, :mod:`zope.deprecation`,
:mod:`zope.i18nmessageid`).  We've been working with the Zope
community to try to collapse and untangle some of these dependencies.
We'd prefer that these packages have fewer packages as transitive
dependencies, and that much of the functionality of these packages was
moved into a smaller *number* of packages.

:mod:`repoze.bfg` also has its own direct dependencies, such as
:term:`Paste`, :term:`Chameleon`, and :term:`WebOb`, and some of these
in turn have their own transitive dependencies.

It should be noted that :mod:`repoze.bfg` is positively lithe compared
to :term:`Grok`, a different Zope-based framework.  As of this
writing, in its default configuration, Grok has 126 package
distribution dependencies. The number of dependencies required by
:mod:`repoze.bfg` is many times fewer than Grok (or Zope itself, upon
which Grok is based).  :mod:`repoze.bfg` has a number of package
distribution dependencies comparable to similarly-targeted frameworks
such as Pylons.

We try not to reinvent too many wheels (at least the ones that don't
need reinventing), and this comes at the cost of some number of
dependencies.  However, "number of package distributions" is just not
a terribly great metric to measure complexity.  For example, the
:mod:`zope.event` distribution on which :mod:`repoze.bfg` depends has
a grand total of four lines of runtime code.  As noted above, we're
continually trying to agitate for a collapsing of these sorts of
packages into fewer distribution files.

BFG "Cheats" To Obtain Speed
----------------------------

Complaints have been lodged by other web framework authors at various
times that :mod:`repoze.bfg` "cheats" to gain performance.  One
claimed cheating mechanism is our use (transitively) of the C
extensions provided by :mod:`zope.interface` to do fast lookups.
Another claimed cheating mechanism is the religious avoidance of
extraneous function calls.

If there's such a thing as cheating to get better performance, we want
to cheat as much as possible.  We optimize :mod:`repoze.bfg`
aggressively.  This comes at a cost: the core code has sections that
could be expressed more readably.  As an amelioration, we've commented
these sections liberally.

BFG Gets Its Terminology Wrong ("MVC")
--------------------------------------

"I'm a MVC web framework user, and I'm confused.  :mod:`repoze.bfg`
calls the controller a view!  And it doesn't have any controllers."

People very much want to give web applications the same properties as
common desktop GUI platforms by using similar terminology, and to
provide some frame of reference for how various components in the
common web framework might hang together.  But in the opinion of the
author, "MVC" doesn't match the web very well in general. Quoting from
the `Model-View-Controller Wikipedia entry
<http://en.wikipedia.org/wiki/Model–view–controller>`_::

  Though MVC comes in different flavors, control flow is generally as
  follows:

    The user interacts with the user interface in some way (for
    example, presses a mouse button).

    The controller handles the input event from the user interface,
    often via a registered handler or callback and converts the event
    into appropriate user action, understandable for the model.

    The controller notifies the model of the user action, possibly  
    resulting in a change in the model's state. (For example, the
    controller updates the user's shopping cart.)[5]

    A view queries the model in order to generate an appropriate
    user interface (for example, the view lists the shopping cart's     
    contents). Note that the view gets its own data from the model.

    The controller may (in some implementations) issue a general
    instruction to the view to render itself. In others, the view is
    automatically notified by the model of changes in state
    (Observer) which require a screen update.

    The user interface waits for further user interactions, which
    restarts the cycle.

To the author, it seems as if someone edited this Wikipedia
definition, tortuously couching concepts in the most generic terms
possible in order to account for the use of the term "MVC" by current
web frameworks.  I doubt such a broad definition would ever be agreed
to by the original authors of the MVC pattern.  But *even so*, it
seems most "MVC" web frameworks fail to meet even this falsely generic
definition.

For example, do your templates (views) always query models directly as
is claimed in "note that the view gets its own data from the model"?
Probably not.  My "controllers" tend to do this, massaging the data for
easier use by the "view" (template). What do you do when your
"controller" returns JSON? Do your controllers use a template to
generate JSON? If not, what's the "view" then?  Most MVC-style GUI web
frameworks have some sort of event system hooked up that lets the view
detect when the model changes.  The web just has no such facility in
its current form: it's effectively pull-only.

So, in the interest of not mistaking desire with reality, and instead
of trying to jam the square peg that is the web into the round hole of
"MVC", we just punt and say there are two things: the model, and the
view. The model stores the data, the view presents it.  The templates
are really just an implementation detail of any given view: a view
doesn't need a template to return a response.  There's no
"controller": it just doesn't exist.  This seems to us like a more
reasonable model, given the current constraints of the web.

.. _apps_are_extensible:

BFG Applications are Extensible; I Don't Believe In Application Extensibility
-----------------------------------------------------------------------------

Any :mod:`repoze.bfg` application written obeying certain constraints
is *extensible*. This feature is discussed in the :mod:`repoze.bfg`
documentation chapter named :ref:`extending_chapter`.  It is made
possible by the use of the :term:`Zope Component Architecture` and
:term:`ZCML` within :mod:`repoze.bfg`.

"Extensible", in this context, means:

- The behavior of an application can be overridden or extended in a
  particular *deployment* of the application without requiring that
  the deployer modify the source of the original application.

- The original developer is not required to anticipate any
  extensibility plugpoints at application creation time to allow
  fundamental application behavior to be overriden or extended.

- The original developer may optionally choose to anticipate an
  application-specific set of plugpoints, which will may be hooked by
  a deployer.  If he chooses to use the facilities provided by the
  ZCA, the original developer does not need to think terribly hard
  about the mechanics of introducing such a plugpoint.

Many developers seem to believe that creating extensible applications
is "not worth it".  They instead suggest that modifying the source of
a given application for each deployment to override behavior is more
reasonable.  Much discussion about version control branching and
merging typically ensues.

It's clear that making every application extensible isn't required.
The majority of web applications only have a single deployment, and
thus needn't be extensible at all.  However, some web applications
have multiple deployments, and some have *many* deployments.  For
example, a generic "content management" system (CMS) may have basic
functionality that needs to be extended for a particular deployment.
That CMS system may be deployed for many organizations at many places.
Some number of deployments of this CMS may be deployed centrally by a
third party and managed as a group.  It's useful to be able to extend
such a system for each deployment via preordained plugpoints than it
is to continually keep each software branch of the system in sync with
some upstream source: the upstream developers may change code in such
a way that your changes to the same codebase conflict with theirs in
fiddly, trivial ways.  Merging such changes repeatedly over the
lifetime of a deployment can be difficult and time consuming, and it's
often useful to be able to modify an application for a particular
deployment in a less invasive way.

If you don't want to think about :mod:`repoze.bfg` application
extensibility at all, you needn't.  You can ignore extensibility
entirely.  However, if you follow the set of rules defined in
:ref:`extending_chapter`, you don't need to *make* your application
extensible: any application you write in the framework just *is*
automatically extensible at a basic level.  The mechanisms that
deployers use to extend it will be necessarily coarse: typically,
views, routes, and resources will be capable of being overridden,
usually via :term:`ZCML`. But for most minor (and even some major)
customizations, these are often the only override plugpoints
necessary: if the application doesn't do exactly what the deployment
requires, it's often possible for a deployer to override a view,
route, or resource and quickly make it do what he or she wants it to
do in ways *not necessarily anticipated by the original developer*.
Here are some example scenarios demonstrating the benefits of such a
feature.

- If a deployment needs a different styling, the deployer may override
  the main template and the CSS in a separate Python package which
  defines overrides.

- If a deployment needs an application page to do something
  differently needs it to expose more or different information, the
  deployer may override the view that renders the page within a
  separate Python package.

- If a deployment needs an additional feature, the deployer may add a
  view to the override package.

As long as the fundamental design of the upstream package doesn't
change, these types of modifications often survive across many
releases of the upstream package without needing to be revisited.

Extending an application externally is not a panacea, and carries a
set of risks similar to branching and merging: sometimes major changes
upstream will cause you to need to revisit and update some of your
modifications.  But you won't regularly need to deal wth meaningless
textual merge conflicts that trivial changes to upstream packages
often entail when it comes time to update the upstream package,
because if you extend an application externally, there just is no
textual merge done.  Your modifications will also, for whatever its
worth, be contained in one, canonical, well-defined place.

Branching an application and continually merging in order to get new
features and bugfixes is clearly useful.  You can do that with a
:mod:`repoze.bfg` application just as usefully as you can do it with
any application.  But deployment of an application written in
:mod:`repoze.bfg` makes it possible to avoid the need for this even if
the application doesn't define any plugpoints ahead of time.  It's
possible that promoters of competing web frameworks dismiss this
feature in favor of branching and merging because applications written
in their framework of choice aren't extensible out of the box in a
comparably fundamental way.

While :mod:`repoze.bfg` application are fundamentally extensible even
if you don't write them with specific extensibility in mind, if you're
moderately adventurous, you can also take it a step further.  If you
learn more about the :term:`Zope Component Architecture`, you can
optionally use it to expose other more domain-specific configuration
plugpoints while developing an application.  The plugpoints you expose
needn't be as coarse as the ones provided automatically by
:mod:`repoze.bfg` itself.  For example, you might compose your own
:term:`ZCML` directive that configures a set of views for a prebaked
purpose (e.g. ``restview`` or somesuch) , allowing other people to
refer to that directive when they make declarations in the
``configure.zcml`` of their customization package.  There is a cost
for this: the developer of an application that defines custom
plugpoints for its deployers will need to understand the ZCA or he
will need to develop his own similar extensibility system.

Ultimately, any argument about whether the extensibility features lent
to applications by :mod:`repoze.bfg` are "good" or "bad" is somewhat
pointless. You needn't take advantage of the extensibility features
provided by a particular :mod:`repoze.bfg` application in order to
affect a modification for a particular set of its deployments.  You
can ignore the application's extensibility plugpoints entirely, and
instead use version control branching and merging to manage
application deployment modifications instead, as if you were deploying
an application written using any other web framework.

The Name BFG Is Not Safe For Work
---------------------------------

"Big Friendly Giant" is not safe for your work?  Where do you work? ;-)

The BFG API Isn't "Flat"
------------------------

The :mod:`repoze.bfg` API is organized in such a way that API imports
must come from submodules of the ``repoze.bfg`` namespace.  For
instance:

.. code-block:: python
   :linenos:

   from repoze.bfg.settings import get_settings
   from repoze.bfg.url import model_url

Some folks understandably don't want to think about the submodule
organization, and would rather be able to do:

.. ignore-next-block
.. code-block:: python
   :linenos:

   from repoze.bfg import get_settings
   from repoze.bfg import model_url

This would indeed be nice.  However, the ``repoze.bfg`` Python package
is a `namespace package <http://www.python.org/dev/peps/pep-0382/>`_.
The ``__init__.py`` of a namespace package cannot contain any
meaningful code such as imports from submodules which would let us
form a flatter API.  Sorry.

Though it makes the API slightly "thinkier", making the ``repoze.bfg``
package into a namespace package was an early design decision, which
we believe has paid off.  The primary goal is to make it possible to
move features *out* of the core ``repoze.bfg`` distribution and into
add-on distributions without breaking existing imports.  The
``repoze.bfg.lxml`` distribution is an example of such a package: this
functionality used to live in the core distribution, but we later
decided that a core dependency on ``lxml`` was unacceptable.  Because
``repoze.bfg`` is a namespace package, we were able to remove the
``repoze.bfg.lxml`` module from the core and create a distribution
named ``repoze.bfg.lxml`` which contains an eponymous package.  We
were then able, via our changelog, to inform people that might have
been depending on the feature that although it no longer shipped in
the core distribution, they could get it back *without changing any
code* by adding an ``install_requires`` line to their application
package's ``setup.py``.

Often new :mod:`repoze.bfg` features are released as add-on packages
in the ``repoze.bfg`` namespace.  Because ``repoze.bfg`` is a
namespace package, if we want to move one of these features *in* to
the core distribition at some point, we can do so without breaking
code which imports from the older package namespace.  This is
currently less useful than the ability to move features *out* of the
core distribution, as :mod:`setuptools` does not yet have any concept
of "obsoletes" metadata which we could add to the core distribution.
This means it's not yet possible to declaratively deprecate the older
non-core package in the eyes of tools like ``easy_install``, ``pip``
and ``buildout``.

Zope 3 Enforces "TTW" Authorization Checks By Default; BFG Does Not
-------------------------------------------------------------------

Challenge
+++++++++

:mod:`repoze.bfg` performs automatic authorization checks only at
:term:`view` execution time.  Zope 3 wraps context objects with a
`security proxy <http://wiki.zope.org/zope3/WhatAreSecurityProxies>`,
which causes Zope 3 to do also security checks during attribute
access.  I like this, because it means:

#) When I use the security proxy machinery, I can have a view that
   conditionally displays certain HTML elements (like form fields) or
   prevents certain attributes from being modified depending on the
   depending on the permissions that the accessing user possesses with
   respect to a context object.

#) I want to also expose my model via a REST API using Twisted Web. If
   If BFG perform authorization based on attribute access via Zope3's
   security proies, I could enforce my authorization policy in both
   :mod:`repoze.bfg` and in the Twisted-based system the same way.

Defense
+++++++

:mod:`repoze.bfg` was developed by folks familiar with Zope 2, which
has a "through the web" security model.  This "TTW" security model was
the precursor to Zope 3's security proxies.  Over time, as the
:mod:`repoze.bfg` developers (working in Zope 2) created such sites,
we found authorization checks during code interpretation extremely
useful in a minority of projects.  But much of the time, TTW
authorization checks usually slowed down the development velocity of
projects that had no delegation requirements.  In particular, if we
weren't allowing "untrusted" users to write arbitrary Python code to
be executed by our application, the burden of "through the web"
security checks proved too costly to justify.  We (collectively)
haven't written an application on top of which untrusted developers
are allowed to write code in many years, so it seemed to make sense to
drop this model by default in a new web framework.

And since we tend to use the same toolkit for all web applications, it's
just never been a concern to be able to use  the same set of
restricted-execution code under two web different frameworks.

Justifications for disabling security proxies by default
notwithstanding, given that Zope 3 security proxies are "viral" by
nature, the only requirement to use one is to make sure you wrap a
single object in a security proxy and make sure to access that object
normally when you want proxy security checks to happen.  It is
possible to override the :mod:`repoze.bfg` "traverser" for a given
application (see :ref:`changing_the_traverser`).  To get Zope3-like
behavior, it is possible to plug in a different traverser which
returns Zope3-security-proxy-wrapped objects for each traversed object
(including the :term:`context` and the :term:`root`).  This would have
the effect of creating a more Zope3-like environment without much
effort.

.. _microframeworks_smaller_hello_world:

Microframeworks Have Smaller Hello World Programs
-------------------------------------------------

Self-described "microframeworks" exist: `Bottle
<http://bottle.paws.de>`_ and `Flask <http://flask.pocoo.org/>`_ are
two that are becoming popular.  `Bobo <http://bobo.digicool.com/>`_
doesn't describe itself as a microframework, but its intended userbase
is much the same.  Many others exist.  We've actually even (only as a
teaching tool, not as any sort of official project) `created one using
BFG <http://bfg.repoze.org/videos#groundhog1>`_. Microframeworks are
small frameworks with one common feature: each allows its users to
create a fully functional application that lives in a single Python
file.

Some developers and microframework authors point out that BFG's "hello
world" single-file program is longer (by about five lines) than the
equivalent program in their favorite microframework.  Guilty as
charged; in a contest of "whose is shortest", BFG indeed loses.

This loss isn't for lack of trying. BFG aims to be useful in the same
circumstance in which microframeworks claim dominance: single-file
applications.  But BFG doesn't sacrifice its ability to credibly
support larger applications in order to achieve hello-world LoC parity
with the current crop of microframeworks.  BFG's design instead tries
to avoid some common pitfalls associated with naive declarative
configuration schemes.  The subsections which follow explain the
rationale.

.. _you_dont_own_modulescope:

Application Programmers Don't Control The Module-Scope Codepath (Import-Time Side-Effects Are Evil)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Please imagine a directory structure with a set of Python files in
it:

.. code-block:: text

    .
    |-- app.py
    |-- app2.py
    `-- config.py

The contents of ``app.py``:

.. code-block:: python

    from config import decorator
    from config import L
    import pprint

    @decorator
    def foo():
        pass

    if __name__ == '__main__':
        import app2
        pprint.pprint(L)

The contents of ``app2.py``:

.. code-block:: python

    import app

    @app.decorator
    def bar():
        pass

The contents of ``config.py``:

.. code-block:: python

    L = []

    def decorator(func):
        L.append(func)
        return func

If we cd to the directory that holds these files and we run ``python
app.py`` given the directory structure and code above, what happens?
Presuably, our ``decorator`` decorator will be used twice, once by the
decorated function ``foo`` in ``app.py`` and once by the decorated
function ``bar`` in ``app2.py``.  Since each time the decorator is
used, the list ``L`` in ``config.py`` is appended to, we'd expect a
list with two elements to be printed, right?  Sadly, no:

.. code-block:: bash

    [chrism@thinko]$ python app.py 
    [<function foo at 0x7f4ea41ab1b8>,
     <function foo at 0x7f4ea41ab230>,
     <function bar at 0x7f4ea41ab2a8>]

By visual inspection, that outcome (three different functions in the
list) seems impossible.  We only defined two functions and we
decorated each of those functions only once, so we believe that the
``decorator`` decorator will only run twice.  However, what we believe
is wrong because the code at module scope in our ``app.py`` module was
*executed twice*.  The code is executed once when the script is run as
``__main__`` (via ``python app.py``), and then it is executed again
when ``app2.py`` imports the same file as ``app``.

What does this have to do with our comparison to microframeworks?
Many microframeworks in the current crop (e.g. Bottle, Flask)
encourage you to attach configuration decorators to objects defined at
module scope.  These decorators execute arbitrarily complex
registration code which populates a singleton registry that is a
global defined in external Python module.  This is analogous to the
above example: the "global registry" in the above example is the list
``L``.

Let's see what happens when we use the same pattern with the
`Groundhog <http://bfg.repoze.org/videos#groundhog1>`_ microframework.
Replace the contents of ``app.py`` above with this:

.. code-block:: python

    from config import gh

    @gh.route('/foo/')
    def foo():
        return 'foo'

    if __name__ == '__main__':
        import app2
        pprint.pprint(L)

Replace the contents of ``app2.py`` above with this:

.. code-block:: python

    import app

    @app.gh.route('/bar/')
    def bar():
        'return bar'

Replace the contents of ``config.py`` above with this:

.. code-block:: python

    from groundhog import Groundhog
    gh = Groundhog('myapp', 'seekrit')

How many routes will be registered within the routing table of the
"gh" Groundhog application?  If you answered three, you are correct.
How many would a casual reader (and any sane developer) expect to be
registered?  If you answered two, you are correct.  Will the double
registration be a problem?  With our fictional Groundhog framework's
``route`` method backing this application, not really.  It will slow
the application down a little bit, because it will need to miss twice
for a route when it does not match.  Will it be a problem with another
framework, another application, or another decorator?  Who knows.  You
need to understand the application in its totality, the framework in
its totality, and the chronology of execution to be able to predict
what the impact of unintentional code double-execution will be.

The encouragement to use decorators which perform population of an
external registry has an unintended consequence: the application
developer now must assert ownership of every codepath that executes
Python module scope code. This code is presumed by the current crop of
decorator-based microframeworks to execute once and only once; if it
executes more than once, weird things will start to happen.  It is up
to the application developer to maintain this invariant.
Unfortunately, however, in reality, this is an impossible task,
because, Python programmers *do not own the module scope codepath, and
never will*.  Microframework programmers therefore will at some point
then need to start reading the tea leaves about what *might* happen if
module scope code gets executed more than once like we do in the
previous paragraph.  This is a really pretty poor situation to find
yourself in as an application developer: you probably didn't even know
you signed up for the job, because the documentation offered by
decorator-based microframeworks don't warn you about it.

Python application programmers do not control the module scope
codepath.  Anyone who tries to sell you on the idea that they do is
simply mistaken.  Test runners that you may want to use to run your
code's tests often perform imports of arbitrary code in strange orders
that manifest bugs like the one demonstrated above.  API documentation
generation tools do the same.  Some (mutant) people even think it's
safe to use the Python ``reload`` command or delete objects from
``sys.modules``, each of which has hilarious effects when used against
code that has import- time side effects.  When Python programmers
assume they can use the module-scope codepath to run arbitrary code
(especially code which populates an external registry), and this
assumption is challenged by reality, the application developer is
often required to undergo a painful, meticulous debugging process to
find the root cause of an inevitably obscure symptom.  The solution is
often to rearrange application import ordering or move an import
statement from module-scope into a function body.  The rationale for
doing so can never be expressed adequnately in the checkin message
which accompanies the fix or documented succinctly enough for the
benefit of the rest of the development team so that the problem never
happens again.  It will happen again next month too, especially if you
are working on a project with other people who haven't yet
internalized the lessons you learned while you stepped through
module-scope code using ``pdb``.

Folks who have a large investment in eager decorator-based
configuration that populates an external data structure (such as
microframework authors) may argue that the set of circumstances I
outlined above is anomalous and contrived.  They will argue that it
just will never happen.  If you never intend your application to grow
beyond one or two or three modules, that's probably true.  However, as
your codebase grows, and becomes spread across a greater number of
modules, the circumstances in which module-scope code will be executed
multiple times will become more and more likely to occur and less and
less predictable.  It's not responsible to claim that double-execution
of module-scope code will never happen.  It will; it's just a matter
of luck, time, and application complexity.

If microframework authors do admit that the circumstance isn't
contrived, they might then argue that "real" damage will never happen
as the result of the double-execution (or triple-execution, etc) of
module scope code.  You would be wise to disbelieve this assertion.
The potential outcomes of multiple execution are too numerous to
predict because they involve delicate relationships between
application and framework code as well as chronology of code
execution.  It's literally impossible for a framework author to know
what will happen in all circumstances ("X is executed, then Y, then X
again.. a train leaves Chicago at 50 mph... ").  And even if given the
gift of omniscience for some limited set of circumstances, the
framework author almost certainly does not have the double-execution
anomaly in mind when coding new features.  He's thinking of adding a
feature, not protecting against problems that might be caused by the
1% multiple execution case.  However, any 1% case may cause 50% of
your pain on a project, so it'd be nice if it never occured.

Responsible microframeworks actually offer a back-door way around the
problem.  They allow you to disuse decorator based configuration
entirely.  Instead of requiring you to do the following:

.. code-block:: python

    gh = Groundhog('myapp', 'seekrit')

    @gh.route('/foo/')
    def foo():
        return 'foo'

    if __name__ == '__main__':
        gh.run()

They allow you to disuse the decorator syntax and go
almost-all-imperative:

.. code-block:: python

    def foo():
        return 'foo'

    gh = Groundhog('myapp', 'seekrit')

    if __name__ == '__main__':
        gh.add_route(foo, '/foo/')
        gh.run()

This is a generic mode of operation that is encouraged in the BFG
documentation. Some existing microframeworks (Flask, in particular)
allow for it as well.  None (other than BFG) *encourage* it.  If you
never expect your application to grow beyond two or three or four or
ten modules, it probably doesn't matter very much which mode you use.
If your application grows large, however, imperative configuration can
provide better predictability.

.. note::

  Astute readers may notice that BFG has configuration decorators too.
  Aha!  Don't these decorators have the same problems?  No.  These
  decorators do not populate an external Python module when they are
  executed.  They only mutate the functions (and classes and methods)
  they're attached to.  These mutations must later be found during a
  "scan" process that has a predictable and structured import phase.
  Module-localized mutation is actually the best-case circumstance for
  double-imports; if a module only mutates itself and its contents at
  import time, if it is imported twice, that's OK, because each
  decorator invocation will always be mutating an independent copy of
  the object its attached to, not a shared resource like a registry in
  another module.  This has the effect that double-registrations will
  never be performed.

Routes (Usually) Need Relative Ordering
+++++++++++++++++++++++++++++++++++++++

Consider the following simple `Groundhog
<http://bfg.repoze.org/videos#groundhog1>`_ application:

.. code-block:: python

    from groundhog import Groundhog
    app = Groundhog('myapp', 'seekrit')

    app.route('/admin')
    def admin():
        return '<html>admin page</html>'

    app.route('/:action')
    def action():
        if action == 'add':
           return '<html>add</html>'
        if action == 'delete':
           return '<html>delete</html>'
        return app.abort(404)

    if __name__ == '__main__':
        app.run()

If you run this application and visit the URL ``/admin``, you will see
"admin" page.  This is the intended result.  However, what if you
rearrange the order of the function definitions in the file?

.. code-block:: python

    from groundhog import Groundhog
    app = Groundhog('myapp', 'seekrit')

    app.route('/:action')
    def action():
        if action == 'add':
           return '<html>add</html>'
        if action == 'delete':
           return '<html>delete</html>'
        return app.abort(404)

    app.route('/admin')
    def admin():
        return '<html>admin page</html>'

    if __name__ == '__main__':
        app.run()

If you run this application and visit the URL ``/admin``, you will now
be returned a 404 error.  This is probably not what you intended.  The
reason you see a 404 error when you rearrange function definition
ordering is that routing declarations expressed via our
microframework's routing decorators have an *ordering*, and that
ordering matters.

In the first case, where we achieved the expected result, we first
added a route with the pattern ``/admin``, then we added a route with
the pattern ``/:action`` by virtue of adding routing patterns via
decorators at module scope.  When a request with a ``PATH_INFO`` of
``/admin`` enters our application, the web framework loops over each
of our application's route patterns in the order in which they were
defined in our module.  As a result, the view associated with the
``/admin`` routing pattern will be invoked: it matches first.  All is
right with the world.

In the second case, where we did not achieve the expected result, we
first added a route with the pattern ``/:action``, then we added a
route with the pattern ``/admin``.  When a request with a
``PATH_INFO`` of ``/admin`` enters our application, the web framework
loops over each of our application's route patterns in the order in
which they were defined in our module.  As a result, the view
associated with the ``/:action`` routing pattern will be invoked: it
matches first.  A 404 error is raised.  This is not what we wanted; it
just happened due to the order in which we defined our view functions.

You may be willing to maintain an ordering of your view functions
which reifies your routing policy.  Your application may be small
enough where this will never cause an issue.  If it becomes large
enough to matter, however, I don't envy you.  Maintaining that
ordering as your application grows larger will be difficult.  At some
point, you will also need to start controlling *import* ordering as
well as function definition ordering.  When your application grows
beyond the size of a single file, and when decorators are used to
register views, the non-``__main__`` modules which contain
configuration decorators must be imported somehow for their
configuration to be executed.

Does that make you a little
uncomfortable?  It should, because :ref:`you_dont_own_modulescope`.

"Stacked Object Proxies" Are Too Clever / Thread Locals Are A Nuisance
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In another manifestation of "import fascination", some microframeworks
use the ``import`` statement to get a handle to an object which *is
not logically global*:

.. code-block:: python

    from flask import request

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error = None
        if request.method == 'POST':
            if valid_login(request.form['username'],
                           request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = 'Invalid username/password'
        # this is executed if the request method was GET or the
        # credentials were invalid    

The `Pylons <http://pylonshq.com>`_ web framework uses a similar
strategy.  It calls these things "Stacked Object Proxies", so, for
purposes of this discussion, I'll do so as well.

Import statements in Python (``import foo``, ``from bar import baz``)
are most frequently performed to obtain a reference to an object
defined globally within an external Python module.  However, in
"normal" programs, they are never used to obtain a reference to an
object that has a lifetime measured by the scope of the body of a
function.  It would be absurd to try to import, for example, a
variable named ``i`` representing a loop counter defined in the body
of a function.  For example, we'd never try to import ``i`` from the
code below:

.. code-block::  python

   def afunc():
       for i in range(10):
           print i

By its nature, the *request* object created as the result of a WSGI
server's call into a long-lived web framework cannot be global,
because the lifetime of a single request will be much shorter than the
lifetime of the process running the framework.  A request object
created by a web framework actually has more similarity to the ``i``
loop counter in our example above than it has to any comparable
importable object defined in the Python standard library or in
"normal" library code.

However, systems which use stacked object proxies promote locally
scoped objects such as ``request`` out to module scope, for the
purpose of being able to offer users a "nice" spelling involving
``import``.  They, for what I consider dubious reasons, would rather
present to their users the canonical way of getting at a ``request``
as ``from framework import request`` instead of a saner ``from
myframework.threadlocals import get_request; request = get_request()``
even though the latter is more explicit.

It would be *most* explicit if the microframeworks did not use thread
local variables at all.  BFG view functions are passed a request
object; many of BFG's APIs require that an explicit request object be
passed to them.  It is *possible* to retrieve the current BFG request
as a threadlocal variable but it is a "in case of emergency, break
glass" type of activity.  This explicitness makes BFG view functions
more easily unit testable, as you don't need to rely on the framework
to manufacture suitable "dummy" request (and other similarly-scoped)
objects during test setup.  It also makes them more likely to work on
arbitrary systems, such as async servers that do no monkeypatching.

Explicitly WSGI
+++++++++++++++

Some microframeworks offer a ``run()`` method of an application object
that executes a default server configuration for easy execution.

BFG doesn't currently try to hide the fact that its router is a WSGI
application behind a convenience ``run()`` API.  It just tells people
to import a WSGI server and use it to serve up their BFG application
as per the documentation of that WSGI server.

The extra lines saved by abstracting away the serving step behind
``run()`` seem to have driven dubious second-order decisions related
to API in some microframeworks.  For example, Bottle contains a
``ServerAdapter`` subclass for each type of WSGI server it supports
via its ``app.run()`` mechanism.  This means that there exists code in
``bottle.py`` that depends on the following modules: ``wsgiref``,
``flup``, ``paste``, ``cherrypy``, ``fapws``, ``tornado``,
``google.appengine``, ``twisted.web``, ``diesel``, ``gevent``,
``gunicorn``, ``eventlet``, and ``rocket``.  You choose the kind of
server you want to run by passing its name into the ``run`` method.
In theory, this sounds great: I can try Bottle out on ``gunicorn``
just by passing in a name!  However, to fully test Bottle, all of
these third-party systems must be installed and functional; the Bottle
developers must monitor changes to each of these packages and make
sure their code still interfaces properly with them.  This expands the
packages required for testing greatly; this is a *lot* of
requirements.  It is likely difficult to fully automate these tests
due to requirements conflicts and build issues.

As a result, for single-file apps, we currently don't bother to offer
a ``run()`` shortcut; we tell folks to import their WSGI server of
choice and run it "by hand".  For the people who want a server
abstraction layer, we suggest that they use PasteDeploy.  In
PasteDeploy-based systems, the onus for making sure that the server
can interface with a WSGI application is placed on the server
developer, not the web framework developer, making it more likely to
be timely and correct.

All of the above said, BFG version 1.3 may offer a ``run()`` - like
shortcut serving API which executes a WSGI server.  But I might also
chicken out and not add it: I'd rather not deal with needing to supply
support answers like `this one
<http://twitter.com/bottlepy/status/20451760706>`_.  If I add such a
method, it will likely be named less attractively to indicate it is
only a shortcut.

:meth:`repoze.bfg.configuration.Configurator.begin` and :meth:`repoze.bfg.configuration.Configurator.end` methods
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The methods :meth:`repoze.bfg.configuration.Configurator.begin` and
:meth:`repoze.bfg.configuration.Configurator.end` are used to bracket
the configuration phase of a :mod:`repoze.bfg` application.

These exist because existing legacy third party *configuration* (not
runtime) code relies on a threadlocal stack being populated. The
``begin`` method pushes data on to a threadlocal stack.  The ``end``
method pops it back off.

For the simplest applications, these lines are actually not required.
I *could* omit them from every BFG hello world app without ill effect.
However, when users use certain configuration methods (ones not
represented in the hello world app), calling code will begin to fail
when it is not bracketed between a ``begin()`` and an ``end()``.  It
is just easier to tell users that this bracketing is required than to
try to explain to them which circumstances it is actually required and
which it is not, because the explanation is often torturous.

The effectively-required execution of these two methods is a wholly
bogus artifact of an early bad design decision which encouraged
application developers to use threadlocal data structures during the
execution of configuration plugins.  However, I don't hate my
framework's users enough to break backwards compatibility for the sake
of removing two boilerplate lines of code, so it stays, at least for
the foreseeable future.  If I eventually figure out a way to remove
the requirement, these methods will turn into no-ops and they will be
removed from the documenation.

Wrapping Up
+++++++++++

Here's a diagrammed version of the simplest repoze.bfg application,
where comments take into account what we've discussed in the
:ref:`microframeworks_smaller_hello_world` section.

.. code-block:: python

   from webob import Response                 # explicit response objects, no TL
   from paste.httpserver import serve         # explicitly WSGI

   def hello_world(request):  # accepts a request; no request thread local reqd
       # explicit response object means no response threadlocal
       return Response('Hello world!') 

   if __name__ == '__main__':
       from repoze.bfg.configuration import Configurator
       config = Configurator()       # no global application object.
       config.begin()                # bogus, but required.
       config.add_view(hello_world)  # explicit non-decorator registration
       config.end()                  # bogus, but required.
       app = config.make_wsgi_app()  # explicitly WSGI
       serve(app, host='0.0.0.0')    # explicitly WSGI

Other Challenges
----------------

Other challenges are encouraged to be sent to the `Repoze-Dev
<http://lists.repoze.org/listinfo/repoze-dev>`_ maillist.  We'll try
to address them by considering a design change, or at very least via
exposition here.
