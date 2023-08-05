collective.amberjack.core
-------------------------

This package provides core functionality for collective.amberjack package.

Be aware that series 0.9.x is compatible with Plone3, series 1.x is compatible
with Plone4.

Useful links
============

- project wiki, info: http://www.coactivate.org/projects/collectiveamberjack
- pypi: http://pypi.python.org/pypi/collective.amberjack.core
- Plone: http://plone.org/products/collective.amberjack.core
- issue tracker: https://bugs.launchpad.net/collective.amberjack
- svn repository: http://svn.plone.org/svn/collective/collective.amberjack.core


How to create new tour
======================

First of all you need to define the tour.

A tour looks like that::

    {'tourId': u'example_tour',
     'title': _(u"Example tour"),
     'steps': <steps>}

a <steps> looks like that::

    ({'url': u'/',
      'xpath': u'',
      'xcontent': u'',
      'title': _(u"Some title"),
      'text': _(u"Some text"),
      'steps': ({'description': _(u"Some description"),
                 'idStep': u'',
                 'selector': u'',
                 'text': u''},
                ...
               )       
     },)                     

                      
Steps parameters:

    * the description for the user (use [] to <span class="ajHighlight">highlight</span> parts), 
    * the step id, [see ajStandardSteps section below]
    * an optional selector
    * an optional text used by the step

An example::

    >>> add_folder = {
    >>>			   'url': u'/',
    >>>            'xpath': u'',
    >>>            'xcontent': u'',
    >>>            'title': _(u"Create a new folder"),
    >>>            'text': _(u"Folders are ..."),
    >>>            'steps': ({'description': _(u"Click the [Add new...] drop-down menu."),
    >>>                       'idStep': u'menu_add-new',
    >>>                       'selector': u'',
    >>>                       'text': u''},
    >>>                      {'description': _(u"Select [Folder] from the menu."),
    >>>                       'idStep': u'new_folder',
    >>>                       'selector': u'',
    >>>                       'text': u''})}
    >>> 
    >>> ajTour = {'tourId': u'basic01_add_a_folder',
    >>>           'title': _(u'Add a Folder'),
    >>>           'steps': (add_folder,
    >>>                    )}


Then you have to register it in zcml::

    <configure 
        xmlns:collective.amberjack="http://namespaces.plone.org/collective.amberjack.core">
        <collective.amberjack:tour
            tourdescriptor=".example_tour.ajTour"
        />
    </configure>


