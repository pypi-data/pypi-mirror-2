Introduction
============

*Note: This code has been merged into Products.Archetypes and will be part of
any Plone 4.1 and later release.*

At the heart of the Archetypes reference engine is the reference_catalog. This
is a set of catalog indexes used to perform the actual query lookups.

The choice of using a ZCatalog has lead to some data structures which aren't
suited for handling references.

This project tries to work around some of the short comings of the internal
implementation of the reference engine without changing the public API or
making any other changes to the stored data.

Development
-----------

The source code can be found at:
https://github.com/hannosch/experimental.atrefspeedup

If you encounter any issues, please contact hanno (at) jarn (dot) com.
