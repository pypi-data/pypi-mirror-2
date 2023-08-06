vs.flexigridsearch
==================

``vs.flexigridsearch`` provides a replacement to the extended search of Plone.
The search results are presented as a sortable table using the jQuery
``flexigrid`` plugin.

Installation
------------
* add ``vs.flexigridsearch`` to the ``eggs`` option of your buildout configuration
  and re-run buildout
* create a new Plone site using the related Plone3 or Plone 4 extension profile of 
  ``vs.flexigridsearch``
* or import the related profile for an existing Plone site through ``portal_setup`` 
  (``Import`` tab)


Usage
-----
* visit the http://host:port/path/to/plone/custom_search URL for your site

Configuration
-------------
* ``vs.flexigridsearch`` uses a property sheet under
  portal_properties/flexigridsearch_properties for its configuration:

  - ``portalTypesToSearch`` - a list of portal types to be searched 
    (a future version of the software will use the configuration of Plone)

  - ``sort_limit`` - maximum number of hits to be retrieved from portal_catalog.
    The parameter name is kind of misleading but the portal_catalog will
    really limit the number of returned rows

  - ``columns`` - defines the columns of the flexigrid table. In general 
    ``vs.flexigridsearch`` can support all searchable indexes of the portal_catalog:

    - getId (this should be always included if you want a clickable link to the content object)
    - Description
    - Title
    - created
    - Creator
    - start
    - end
    - effective
    - expires
    - location
    - Subject
    - getObjSize
    - review_state
    - portal_type

Requirements
------------
* tested with Plone 3.3.X, 4.0.X

Licence
-------
``vs.flexigridsearch`` is published under the GNU Public Licence V 2 (GPL 2)

Authors
-------

| Andreas Jung
| info@zopyx.com
| www.zope.com
|
| Veit Schiele
| kontakt@veit-schiele.de
| www.veit-schiele.de
|
