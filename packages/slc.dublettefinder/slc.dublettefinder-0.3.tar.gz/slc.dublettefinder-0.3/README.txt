Introduction
============

slc.dublettefinder is a Plone product plugin that warns you of possible
file duplications in your Plone website.

It provides custom validators (that can be ignored with a checkbox on the form)
that warns the user if the file or image being uploaded is a possible duplicate
of a file already in the site.

It also provides a portlet that will show any possible file duplications when
on the context of any file or image.

Works with the ATContentTypes ATFile and ATImage as well as Blobs.


Validators:
-----------
Validators are run when an object is newly created or being edited. They are
used to for example check that the fields of the object where correctly filled
in.

slc.dublettefinder registers three new validators for the main two file containing objects
(ATFile and ATImage), and you can easily register them for your own file
containing objects. See ./extensions/configure.zcml

The validators are called isUniqueObjectName, isUniqueFileName and
isUniqueFileSize and can be found in ./validators.py.

The first validator check the object's Title against all other objects of the
same type in the database, and warns you if there is a match.

The second validator checks the uploaded file's name against files in the
database and the third validator checks the file's size.

All three validators will warn you if they find a match, and then allow you to
override them (by clicking a checkbox) and continue adding your object.

Portlet:
--------
A custom portlet is also provided, that will show you any possible duplicates
of the object/context that you are currently viewing.

