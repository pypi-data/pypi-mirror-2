Introduction
============

Character set of outgoing mail from Plone is defined in a portal property name "email_charset" and this charset is globally used in the Plone site.
This is fine with monolingual site, however in multilingual site, there are cases you want to send mails with differernt character sets for different languages.
This package provides this function to Plone-4.x.

This does not have backword compatibility for Plone-3.x, so for those who wants to use this for Plone-3.x, use version 0.2.0.

There are five main default cases for sending e-mails from Plone site:

1. When new user registers to the site with password setting  disabled.
2. When a user forgets password and plone sends the user the guide to reset it.
3. When user contacts administrator form contact form.
4. When content rules trigers sending mail, ex) when adding content to a certain folder.

Tests are only done with character set of iso-2022-jp for Japanese language and utf-8 for other languages.

Installation
============

If you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``collective.langMailHost`` to the list of eggs to install, e.g.:

    |    [buildout]
    |    ...
    |    eggs =
    |        ...
    |        collective.langMailHost

* Tell the plone.recipe.zope2instance recipe to install a ZCML slug:

    |    [instance]
    |    recipe = plone.recipe.zope2instance
    |    ...
    |    zcml =
    |        collective.langMailHost

* Re-run buildout, e.g. with:

    $ ./bin/buildout


Setting language and character set
-------------------------------------------

Once you installed this package from quickinstaller, go to ZMI of the plone site.
Within portal_properties, there is mailhost_properties where you can set two propeties.

* lang_charset
    'ja|iso-2022-jp' is default value.
    This means for Japanese language ('ja'), use character set 'iso-2022-jp'.
    To add other language and character set pair, add it line by line.
    Remenber to follow this syntax: language|charset

* is_member_lang_effective
    If this option is selected, logged in member receives e-mail with the character set of member's choice of languages.


Script example for your own code
----------------------------------------

Here is an example how to use ILangCharset interface:

>>> from collective.langMailHost.interfaces import ILangCharset
>>> charset = ILangCharset(portal).effective_charset() or portal.getProperty('email_charset', 'UTF-8')
...
