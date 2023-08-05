.. contents ::

Introduction
-------------

collective.fastview provides framework level helper code for Plone view and template management.
It is intended to be used with of Plone 3, Zope viewlets and five.grok, 
to workaround some rough corners on these frameworks.

Installation
------------

Add collective.fastview to buildout eggs list::

        eggs = 
                ...
                collective.fastview

Render viewlets without viewlet manager
---------------------------------------

*The method described here is not a correct
approach as viewlet update() method 
might be called several times. It is just a shortcut 
when you need to toss around few vietlets here and there*.

You can directly put in viewlet call to any page template code 
using a viewlet traverser. collective.fastview registers
a view with name @@viewlets which you can use to traverse 
to render any viewlet code::

        <div id="header">
            <div tal:replace="structure context/@@viewlets/plone.logo" />
        </div>

Note that you still need to register viewlets against some viewlet manager,
but it can be a dummy one, which is never rendered directly::

        class MainViewletManager(grok.ViewletManager):
            """ This viewlet manager is responsible for all gomobiletheme.basic viewlet registrations.
        
            Viewlets are directly referred in main_template.pt by viewlet name,
            thus overriding Plone behavior to go through ViewletManager render step.
            """
            grok.name('gomobiletheme.basic.viewletmanager')
        
        # Set viewlet manager default to all following viewlets
        grok.viewletmanager(MainViewletManager)



Fix Grok 1.0 template inheritance
---------------------------------

This fixes grok 1.0 problem that view and viewlets template are not inheritable between packages.
E.g. if you subclass a view you need to manually copy over the view template also.
    
We hope to get rid of this with Plone 4 / fixed grok.
    
See:
    
* https://bugs.launchpad.net/grok/+bug/255005

Example::

        from collective.fastview.utilities import fix_grok_template_inheritance
        from gomobiletheme.basic import viewlets as base
        from gomobiletheme.basic.viewlets import MainViewletManager
        from plonecommunity.app.interfaces import IThemeLayer
        
        # Viewlets are on all content by default.
        grok.context(Interface)
        
        # Use templates directory to search for templates.
        grok.templatedir("templates")
        
        # Viewlets are active only when gomobiletheme.basic theme layer is activated
        grok.layer(IThemeLayer)
        
        grok.viewletmanager(MainViewletManager)
        
        class Head(base.Head):
            """
            My inherited viewlet.
            """
            
          
        # Fix for grok 1.0 template inheritance
        # https://bugs.launchpad.net/grok/+bug/255005
        # This will force Head viewlet to use its parent class template
        fix_grok_template_inheritance(Head, base.Head)

Examples
--------

These Python packages use this code

* http://code.google.com/p/plonegomobile/source/browse/#svn/trunk/gomobile/gomobiletheme.basic/gomobiletheme/basic

Source code repository
-----------------------

* https://svn.plone.org/svn/collective/collective.fastview

Roadmap
-------

* Work around viewlet rendering so that update() method gets called only once
  (not sure if issue currently). Probably needs to create a dummy ViewletManager
  class and instance.


Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
      