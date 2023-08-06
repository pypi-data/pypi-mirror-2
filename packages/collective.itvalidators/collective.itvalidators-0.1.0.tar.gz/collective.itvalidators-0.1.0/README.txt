.. contents:: **Table of contents**

Introduction
============

This product add to Plone some additional `validators`__.

__ http://plone.org/documentation/manual/developer-manual/archetypes/fields/validator-reference

Some of theme can be useful only for Italian users or sites targeted on Italy (as many of the default ones
like ``isSSN``or ``isUSPhoneNumber`` are not useful for non-US sites), other are simply additional validators
that everyone can find useful.

The idea behind the product is simply collect a set of validators that commonly are putted inside other
products, but in this way not easily reusable.

Italian Specific validators
===========================

isCAP
-----

Very similar to the native ``isZipCode`` but this only accept 5 digits values. Formally is
`Codice di Avviamento Postale`__.

__ http://it.wikipedia.org/wiki/Codice_di_avviamento_postale

isItalianNIN
------------

Check if a string is a valid `Italian National Insurance Number`__ ("Codice Fiscale"). The validator only check
the format of the string, not if the string itself is a *real* and existing code.

__ http://it.wikipedia.org/wiki/Codice_fiscale

General purpose validators
==========================

MinCharsValidator
-----------------

This validator test if the given value is at least a specific number of characters long. The default
character value is 500.

The validator will also ignore any whitespace (space character, carriage return, tab...) so the text::

    Hello World

is long like::

    Hello      World

and also long like::

    Hello   
    
         World

How to use
~~~~~~~~~~

An example::

    from collective.itvalidators.validators import MinCharsValidator
    ...
    
    TextField('text',
              validators = (MinCharsValidator()),
    ),

To customize the number of characters::

    TextField('text',
              validators = (MinCharsValidator(100)),
    ),

You can also threat is a special way HTML text (for example, if it came from TinyMCE) beeing sure that only
content characters (not HTML tags) are counted. Example::

    TextField('text',
              default_output_type = 'text/x-html-safe',
              validators = ('isTidyHtmlWithCleanup', MinCharsValidator(100, strict=True)),
    ),


Contribute!
===========

You are welcome to add to this product your additional validation (also some unit-tests for every new validator
are welcome)! Contact us at sviluppoplone@redturtle.it

You can also contribute providing new translation for validation messages.

Credits
=======

Developed with the support of `Azienda USL Ferrara`__; Azienda USL Ferrara supports the
`PloneGov initiative`__.

.. image:: http://www.ausl.fe.it/logo_ausl.gif
   :alt: Azienda USL's logo

__ http://www.ausl.fe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

