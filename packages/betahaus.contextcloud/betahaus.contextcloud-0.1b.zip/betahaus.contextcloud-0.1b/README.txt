Betahaus ContextCloud
=====================

* `Introduction`_
* `Usage`_
* `Caveats`_
* `Found a bug?`_
* `Contributors`_


Introduction
------------

A simple tag cloud or list that shows what's in this context. It's only usable
for folderish things including collections. If you combine several portlets
it will work like a facet navigation. It doesn't require any customisation or
customized listing templates - it should just work with whatever you have in place
or the Plone default ones.

The tag cloud uses the power law to normalize sizes. In most usecases when tags
are folksonomy-based it should cause the most used tags to have a bit less weight
proportionally to the other tags.

The package itself consists of an adapter that does all computing (to make it simple
to use it for other things) and a portlet that displays stuff.


Usage
-----

* Install the product (in buildout and in Plone)
* Go to manage portlets and select "Context cloud portlet".
* Catalog index is the index to build results from. It has to exist as a column
  in the portal catalog. (It won't be selectable here if it doesn't)
* Cloud shows results as a tag cloud.
* List shows it as a list with the number of occurences to the right.
* Level is only used for tag clouds. It sets how many different levels (sizes)
  it should have. If you use more than 5 you need to add css for it. (see the css file)
* The portlet will show up in any folderish context with at least 1 result for the
  catalog index you selected.
* That's it.


Caveats
-------

* I didn't want to add any caching at this stage. It doesn't make sense unless you have
  an enormous amount of hits and content, and in that case you'll have Varnish or something
  else in front anyway, right?


Found a bug?
------------

Please contact the author at robin (at) betahaus.net

If you want to participate in development of this or any other project that Betahaus does,
check out http://dev.betahaus.net.


Contributors
------------

* `Robin Harms Oredsson <http://www.betahaus.net/>`_, Author / Swedish translation.
* Veronika Menjoun, Russian translation.
* `FOJO <http://http://www.fojo.se/>`_, Funding

.. image:: http://betahaus.net/logo.jpg
   :alt: Betahaus logo
   :target: http://betahaus.net

Made by `Betahaus <http://www.betahaus.net>`_
- if you want to contribute, visit `http://dev.betahaus.net <http://dev.betahaus.net>`_
