Photofile
=========

Version : 0.1.0
Author : Thomas Weholt <thomas@weholt.org>
License : GPL v3.0
WWW : https://bitbucket.org/weholt/django-photofile
Status : Experimental


About
-----
* Templatetags for thumbnail generation, supports automatic rotation based on EXIF.Orientation.
* Planned routines for metadata handling (EXIF/IPTC/XMP).

How
---
    <img src="{% generate_thumbnail imagefile 100x100 crop %}"/>

Provides a templatetag called generate_thumbnail which takes two or three parameters:

Param #1 : an object (imagefile), like a model instance, with a property/field called unique_filename, complete_filename or filename.
Photofile will check in that order.

Param #2: resolution, specified as <width>x<height>, like 320x280.

Param #3: optional "crop" - which will enforce cropping of the photo.

The thumbnail will be written in a dir called "thumbs" in your STATICFILES_DIRS or STATIC_ROOT. If no dir exists
called thumbs, it will be created.

The generated thumbnail will be named <filename>_<width>x<height>.<extension>. When cropping is used it will be named
<filename>_<width>x<height>_crop.<extension>. For instance, thumbnail for test.jpg in resolution 200x300 will be named
test_200x300.jpg.

Photofile will try to use caching if enabled, but it caches the url to the thumbnail, not the image itself so it's not
very efficient yet.

NB! It's highly recommended to have some way of ensuring that the filename given to photofile is unique. That's why it will
look for a property called unique_filename first. 

Why another thumbnail app for django?
-------------------------------------
I've looked at sorl-thumbnail and others, and initially I wanted to use an existing project, but none of them supported
automatic rotation based on EXIF.Orientation.

Installation
------------
* Alternative a) pip install django-photofile.
* Alternative b) download source, unpack and do python setup.py install.
* Alternative c) hg clone https://bitbucket.org/weholt/django-photofile and do python setup.py install.

Usage
-----
In settings.py:
* Add 'photofile' to your INSTALLED_APPS.
* Set up caching if you want.
* Add a dir to your STATICFILES_DIRS or set STATIC_ROOT.

In your template:
     {% load photofile_tags %}

     <img src="{% generate_thumbnail imagefile 200x300 %}"/>
or
     <img src="{% generate_thumbnail imagefile 100x100 crop %}"/>

Where imagefile is an object with at a property/field called:
* unique_filename or
* complete_filename or
* filename

Resolution is specified as <width>x<height>, for instance 640x480 and if you want to crop the photo add crop as shown in
the example over.

Requirements
------------
* django
* PIL