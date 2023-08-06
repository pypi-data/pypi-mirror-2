Introduction
============

The Oracle is a debug/development helper app for Plone.  It currently shows 
the following information about a given user/context:

* Authenticated User Info - ID, member type, roles, etc.
* Basic Context Info - ID, portal_type, path, absolute_url, etc.
* Context Workflow Info - Review state, history, assigned workflow
* Catalog Indexes
* Catalog Metadata
* Methods - Including security declarations
* Attributes - including values
* Valid/Invalid permissions (including security settings)
* Context source code
* Browser view registrations on context
* Request content

It also provides a fast way to drop to PDB at any given context.

Installation/Use
================

To install, just stick it in your buildout, once you've got your instance
running, there's a few of views which you can use:

* the_oracle - This is the main tool
* opdb - Drops you to pdb at the current context (self.context)

Top Tip
=======
If the Context Fields section isn't showing enough information about
the object schema, try adding ?extras=True to the url.  This will
show extended information (Searchable, Mode, Index and Edit Accessors, Vocabulary).

A Friendly Warning
==================

DO NOT LEAVE THIS PRODUCT INSTALLED ON A PRODUCTION SITE! IT MASSIVELY
UNDERMINES THE SECURITY OF THE SITE IT'S INSTALLED ON, AND IS VISIBLE 
TO ANY USER (EVEN ANONYMOUS).  ALSO, BEARS WITH ASSAULT RIFLES WILL 
COME TO YOUR HOUSE AND ROUGH YOU UP IF YOU DO.  TAKE A MOMENT TO THINK
ABOUT THAT. BEARS. ANGRY BEARS. WITH GUNS. IN YOUR KITCHEN. EATING YOUR
DINNER.