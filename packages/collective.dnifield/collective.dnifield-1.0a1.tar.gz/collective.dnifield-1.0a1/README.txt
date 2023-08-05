Introduction
============

This is a zope.schema field to enter national identification
numbers. For now, it just supports Spanish ones in the format
12345678X, where X is the verification letter.

If the verification letter is supplied, it will be checked, but
numbers without letter are accepted too.
