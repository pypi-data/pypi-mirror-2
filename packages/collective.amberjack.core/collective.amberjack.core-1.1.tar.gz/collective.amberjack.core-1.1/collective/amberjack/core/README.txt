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

First of all you need to define the tour. Starting version 1.1 we are using
configuration based style.

A tour is a .cfg file. It has an ``amberjack`` main section which
has two options: ``title`` and ``steps`` - this is where you define tour steps::

    [amberjack]
    steps = 
        my_step1
        my_step2
    title = My first amberjack tour

there are also available two blueprints:
1. Step
a ``step`` section is defined by ``collective.amberjack.blueprints.step`` and
has several options: 

  * ``title``
  * ``text``
  * ``url`` - step url definition
  * ``xpath`` - xpath selector
  * ``xcontent`` - xcontent selector
  * ``microsteps`` - microsteps sections
  * ``validators`` - tales expression validation

it looks like that::

    [my_step1]
    blueprint = collective.amberjack.blueprints.step
    title = This is my first Step
    text = You should now know how to create a step section
    url = /mystep
    validators =
        python: context.isFolderish()
    xpath = ''
    xcontent = ''
    microsteps = 
        microstep_1
        microstep_2

2. Microstep
a ``microstep`` section is defined by ``collective.amberjack.blueprints.microsteps`` 
and it has several options:

  * ``idstep``
  * ``text``
  * ``description``
  * ``selector``

it looks like that::

    [microstep_1]
    blueprint = collective.amberjack.blueprints.microstep
    idstep = menu_state
    text = This is my dummy microstep
    description = Now you should now how to define microsteps
    selector = #insert


Tour registration
=================

Finally you have to register it. The only acceptable format is an archive 
(zip or tar) which contains one or multiple .cfg files (tours)
Using zcml::

    <configure 
        xmlns:collective.amberjack="http://namespaces.plone.org/collective.amberjack.core">
        <collective.amberjack:tour
            tourlocation="mytourpackage.zip"
        />
    </configure>
