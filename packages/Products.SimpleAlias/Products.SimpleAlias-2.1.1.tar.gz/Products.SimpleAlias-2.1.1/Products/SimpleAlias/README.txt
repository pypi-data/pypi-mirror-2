===========
SimpleAlias
===========

Requirements
============

This components requires Plone 3.0 or better.

What is SimpleAlias?
====================

SimpleAlias is a product that let's you create aliases or shortcuts to content
somewhere in your portal.  It behaves similar to an alias in the filesystem. In
many cases you want to have such a link in a folder to some object elsewhere in
the portal without having to recreate that object. Of course you can use the
Link object but that is rather primitive.

SimpleAlias introduces a new content type: Alias. Once you create the Alias, you
can create a reference to another object in the portal and the Alias will copy
the title and description of this target object.  When you view the alias, it
shows the object within the context of the Alias and it presents the user a link
to the target object itself. So, no scary traversal tricks. You remain in the
context of the Alias.

Another way to create an Alias to an object is to copy that object in the
contents view of the objects container and then to go to the location where you
want to Alias and click on 'Paste as alias' in the contents view.

It's as simple as that. SimpleAlias can only link to AT 1.3+ based objects so to
make real use of it you will need ATContentTypes.

Installation
============

``Products.SimpleAlias`` is available as egg. So you can just install it using
``pip`` or ``easy_install``.

To install it using ``zc.buildout``, just add this line in the
``plone.recipe.zope2instance`` part of your ``buildout.cfg`` ::

  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      Products.SimpleAlias

Ans, of course, re-run your buildout.


simplealias_tool
================

In the root of your portal, in ZMI, a new tool is created. This tool allows you
to filter portal types to which you cannot create a link to. It only filters the
Target object list in the edit view of the Alias.

The content icons
=================

An Alias uses the target object's icon. If there is an alias-variant for this
icon then SimpleAlias will use that instead.  That works as follows: Suppose the
target object's icon is **document_icon.gif**. If there exists an icon with id
**document_icon_alias.gif**, SimpleAlias will use that icon instead. SimpleAlias
comes with alias icons for the common Plone icons but of course you can create
them yourself. In the SimpleAlias skinfolder there is a gif alias-arrow.gif. You
can overlay that over your icon (preferably in the lower-right corner, with one
pixel space to the right and bottom). Save it as &lt;original icon
name&gt;_alias.gif.  SimpleAlias will use that if it can find it.

Permissions
===========

Since there is hardly any trickery in SimpleAlias, there is one security issue
you have to be aware of: If you create an Alias that points to a target object
in a restricted area of your portal then a user who has view permissions for the
Alias and not for the target object WILL see the title and description of the
target object. Think about that for a while. So, the Alias will cache/show the
title and description of the target, no matter what, when the user may view the
Alias. So you will have to be aware of this when you create the Alias.

Folderishness
=============

An Alias mimicks the folderishness of the target object. If the target object is
a folder then the attribute isPrincipiaFolderish will return 1 for the Alias
eventhough it is not folderish itself.  By doing this, the Alias object will be
visible in the navigation portlet if the target is folderish.  The only downside
(as far as I can see) is that sometimes you get a folder_contents view of the
Alias without contents (since the Alias itself is not really folderish). Pff,
well, it's not as complicated as this paragraph itself ;-)

Limitations
===========

The view of content types that have no "main" macro, may be ugly. Sorry but we
can't find an easy workaround. You just need to add such content types in the
'portal_type_filters" property of the 'simplealias_tool' object in ZMI.

Feedback
========

Please send your feedback to danny dot bloemendaal at companion dot
nl, or use the tracker available from
http://plone.org/products/simplealias

Releases
========

You may find newer releases of SimpleAlias at
http://plone.org/products/simplealias or
http://pypi.python.org/pypi/Products.SimpleAlias . But you're certainly reading
one of these pages.

