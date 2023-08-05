Introduction
============

A Plone portlet that uses the catalog internals to find 'similar' content to the page you are looking at

This portlet uses some deep dark data structures within the ZCatalog and ZCTextindex, so it could be brittle in the future
if those structures are changed. Then again, they have been the same for the past 8 years or so ;)

This portlet also runs in linear time relative to the number for documents you have in your site, so
it could well slow things down. That said I've tried to make it pretty efficient.

TODO:
Add some caching ;)

