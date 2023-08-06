
=====
Usage
=====

This section contains information, including examples, about how to use
*django-content-licenses* in your existing Django projects or applications.


The LicenseField
================

.. autoclass:: content_licenses.fields.LicenseField


Template Variables
==================

Expected context (template variables):

- content_title
- content_url
- author_name
- author_url
- license_name
- license_url
- extra_perms_title
- extra_perms_url
- template_name
- pubdate
- semantics
