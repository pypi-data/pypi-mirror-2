=================
 iBase Interface
=================

.. module:: itaps.iBase
   :synopsis: Utilities and definitions used in multiple ITAPS core interfaces.

iBase Types
===========

.. class:: ITAPSError

   The exception type used for all internal ITAPS errors.

.. class:: Base

   The base class for all PyTAPS interfaces (e.g. :class:`itaps.iMesh.Mesh`).

.. class:: Entity

   An individual entity from a specific interface.

.. class:: EntitySet

   The base class for all interface-specific entity set types (e.g.
   :class:`itaps.iMesh.EntitySet`).

.. class:: Tag

   The base class for all interface-specific tag types (e.g.
   :class:`itaps.iMesh.Tag`).

Enumerations
============

.. class:: Type

   An enumeration of entity types corresponding to ``iBase_EntityType``.

   .. data:: vertex

      A zero-dimensional entity

   .. data:: edge

      A one-dimensional entity

   .. data:: face

      A two-dimensional entity

   .. data:: region

      A three-dimensional entity

   .. data:: all

      Allows the user to request information about all the types

.. class:: AdjCost

   An enumeration of entity types corresponding to ``iBase_AdjacencyCost``.

   .. data:: unavailable

      Adjacency information not supported

   .. data:: all_order_1

      No more than local mesh traversal required

   .. data:: all_order_logn

      Global tree search

   .. data:: all_order_n

      Global exhaustive search

   .. data:: some_order_1

      Only some adjacency info, local

   .. data:: some_order_logn

      Only some adjacency info, tree

   .. data:: some_order_n

      Only some adjacency info, exhaustive

.. class:: StorageOrder

   An enumeration of entity types corresponding to ``iBase_StorageOrder``.

   .. data:: interleaved

      Coordinates are interleaved, e.g. ((x\ :sub:`1`\, y\ :sub:`1`\,
      z\ :sub:`1`\), (x\ :sub:`2`\, y\ :sub:`2`\, z\ :sub:`2`\), ...). This is
      the default.

   .. data:: blocked

      Coordinates are blocked, e.g. ((x\ :sub:`1`\, x\ :sub:`2`\, ...),
      (y\ :sub:`1`\, y\ :sub:`2`\, ...), (z\ :sub:`1`\, z\ :sub:`2`\, ...)).

.. class:: CreationStatus

   An enumeration of entity types corresponding to ``iBase_CreationStatus``.

   .. data:: new

      New entity was created

   .. data:: exists

      Entity already exists

   .. data:: duplicated

      Duplicate entity created

   .. data:: failed

      Creation failed
