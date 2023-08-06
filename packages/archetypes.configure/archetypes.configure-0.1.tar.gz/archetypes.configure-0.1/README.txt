Introduction
============

This package adds a declarative interface for the registration of
Archetypes content classes.

Usage
-----

Use an ``at:register`` directive to register each of your content
classes.

Example configuration::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:at="http://namespaces.plone.org/archetypes">

      <five:registerPackage package="." />

      <permission id="example.Add" title="collective.example: Add example" />

      <at:register
          class=".content.Example"
          permission="example.Add"
          />

    </configure>

You do not need to (and should not) call ``atapi.registerType`` on
your content classes. This is done automatically by the framework.

Credits
-------

Malthe Borch <mborch@gmail.com>
