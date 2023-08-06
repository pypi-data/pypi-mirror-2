
Introduction
------------

This package provides functionality to ease skinning of plone.
It is built around the idea that you shouldn't have to adapt much plone
templates but instead take any layout you want and put it on top of Plone.

That means that all editing is done using Plone skin but for anonymous users
(or users not having the correct permission) another skin is shown. This works
based on rules described below. No url switching or iframe magic needed.

It resembles *collective.skinny* but instead of imposing customized templates
for each and every content type this package tries to reuse already
existing views and templates. You also won't need a special server
configuration to redirect to ++skin++ or such. With some coding it is also
possible to use this for community sites because people *can* log in and
either (if permission is set) they see the well-known Plone interface or the public skin.
Also there is no need to hack around to prevent plone templates from
``leaking`` because you *want* to display all plone related templates as is.

Full Example provided here: http://pypi.python.org/pypi/anthill.exampletheme

Installation
------------

- Include anthill.skinner in your buildout.cfg
- Make sure to also include z3c.autoinclude
- Rerun buildout
- Restart your Zope instance
- Go to portal_quickinstaller and install anthill.skinner
- ATT: Make sure to restart Zope - this is because of a handler only being
  evaluated on startup
- There should be a new link "Show Preview" on the bottom

Creation of a theme (simple way)
--------------------------------

- Create a new folder custom_public in portal_skins
- Include this folder in portal_skins/manage_propertiesForm in publicview
- Customize anthill_skinner_templates/main_template to custom_public
- Put images and CSS also to this folder
- For a more elaborate example look at anthill.exampletheme

Dependencies
------------

- z3c.autoinclude
- anthill.tal.macrorenderer

Tested with
-----------

- Plone 4.x (for Plone 3.x use version <0.7)

Pros
----

 - No need to understand the complex plone template logic
 - No need to write a new handbook for editors - take any recent plone book
   because the edit skin stays the same
 - Less work when updating to a new Plone version because you didn't touch
   much of the templates
 - Almost no limitations for your theme/design that could be imposed by the
   fact that you need to include all the edit functionality (tabs, ...) into
   your theme
 - By not having to fiddle with Plone inner logic/templates that much you save
   much time

Cons
----

 - Editors have no in-place editing - although you can change to the edit view
   on every context there's one more click needed
 - Including plone portlets into your theme is a little more complex

Similar packages
----------------

 - collective.skinny
 - collective.editskinswitcher

Rules
-----

Instead of having url based rules this package uses simple rules suitable for
most deployments. If you don't like these rules then you can easily overwrite
them.

Rules to show public skin are as follows (order matters):

 - User is anonymous
 - User is authenticated but has not the correct permission (anthill: View CMS)
 - User is authenticated, has the correct permission but activated preview
 - There is a request variable named anthill.skinner.preview

All rules can be found in ``browser/handling#mustDisplayPublicSkin.``
 
Overwrite rules
---------------

You can overwrite these rules by defining an adapter. Please keep in mind that if
you overwrite rules then you need to overwrite all rules!

configure.zcml::

    <adapter
        for="anthill.skinner.interfaces.ISkinHandler"
        provides="anthill.skinner.interfaces.IRuleOverwrite"
        factory="your.product.publicview.RuleMaker"
    />

publicview.py::

    class RuleMaker:
        implements(IRuleOverwrite)

        def __init__(self, context):
            self.context = context

        def mustDisplayPublicView(self, context, request):
            return True

How to create your own skin
---------------------------

In order to create your own skin first take a look at the very simple example
included in this package. It shows you how to define your menu and how content
will be displayed.

Please be aware of the fact that it is intended to not load any of the css or
javascript coming with Plone.

You can then create your own theme based on anthill.skinner by simply using the
same skin and layer for your resources. Use ``anthill.skinner.interfaces.IPublicSkinLayer`` 
as the layer and ``publicview`` as the skin name you're putting your stuff into.

Thanks
------

- Developers of collective.skinny
- Plone community
- banality design & communication for funding this (all anthill.* packages)

This package is part of the anthill.* ecosystem that powers many websites all
around the world - all being built on top of this package (originally for
Plone 2.x).

