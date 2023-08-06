================
 iRel Interface
================

.. module:: itaps.iRel
   :synopsis: Basic services to relate entities and sets in pairs of interfaces.

Rel
===

.. autoclass:: Rel([options])

   .. automethod:: createPair(first,first_type,second,second_type)
   .. automethod:: destroyPair(pair)
   .. automethod:: findPairs(interface)

Pair
====

.. autoclass:: Pair

   .. autoattribute:: instance
   .. autoattribute:: first
   .. autoattribute:: second
   .. autoattribute:: firstType
   .. autoattribute:: secondType
   .. automethod:: setRelation(first, second)
   .. automethod:: getEntRelation([first, second])
   .. automethod:: getEntArrRelation([first, second])
   .. automethod:: getSetRelation([first, second])
   .. automethod:: getSetArrRelation([first, second])
   .. automethod:: inferAllRelations()
   .. automethod:: inferRelations([first, second])

Enumerations
============

.. class:: Type

   An enumeration of mesh element topologies corresponding to
   ``iRel_RelationType``.

   .. data:: entity

      TODO

   .. data:: set

      TODO

   .. data:: both

      TODO
