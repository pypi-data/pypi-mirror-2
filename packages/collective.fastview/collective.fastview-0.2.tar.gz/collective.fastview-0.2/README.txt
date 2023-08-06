.. contents ::

Introduction
-------------

collective.fastview provides framework level helper code for Plone view and template management.
It is intended to be used to give some workarounds some rough corners on these Zope 3
and `five.grok <http://pypi.python.org/pypi/five.grok>`_ viewlewt frameworks.

Installation
------------

Add collective.fastview to buildout eggs list::

        eggs = 
                ...
                collective.fastview

Render viewlets directly anywhere in the template
---------------------------------------------------

You can directly put in viewlet call to any page template code 
using a viewlet traverser. ``collective.fastview`` registers
a view with name ``@@viewlets`` which you can use to traverse 
to render any viewlet code::

        <div id="header">
            <div tal:replace="structure context/@@viewlets/plone.logo" />
        </div>

Note that you still need to register viewlets against some (any) viewlet manager,
but it can be a dummy one, which is never rendered using syntax::

        <div tal:replace="structure provider:myarghyetanotherviewletmanagername" />

Example of dummy viewlet manager::

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
    
We hope to get rid of this in the future.
    
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

This code is mainly used with ``gomobiletheme.basic`` package
to provide simple mobile themes without need to construct viewlet manager
around every viewlet.

* http://webandmobile.mfabrik.com

These Python packages use this code

* http://code.google.com/p/plonegomobile/source/browse/#svn/trunk/gomobile/gomobiletheme.basic/gomobiletheme/basic

Source code repository
-----------------------

* https://svn.plone.org/svn/collective/collective.fastview

Author
------

`mFabrik Research Oy <mailto:research@mfabrik.com>`_ - Python and Plone professionals for hire.

* `Web and mobile project - mobilize your Plone site in an instant <http://webandmobile.mfabrik.com>`_

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
      