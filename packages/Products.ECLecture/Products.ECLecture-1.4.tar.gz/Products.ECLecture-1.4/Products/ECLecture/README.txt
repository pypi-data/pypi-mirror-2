Overview
========

ECLecture is a Plone product for managing lectures, seminars and 
other courses.


Download
========

`plone.org products page`_

.. _plone.org products page: http://plone.org/products/eclecture/


Prerequisites
=============

- Plone_: 4.x

- DataGridField_: 1.6 or newer

.. _Plone: http://plone.org/products/
.. _DataGridField: http://plone.org/products/datagridfield/


Installation
============

See the `Installing an Add-on Product`_ tutorial for more detailed 
product installation instructions.
        
.. _Installing an Add-on Product: http://plone.org/documentation/tutorial/third-party-products/installing


Installing with buildout
------------------------

If you are using `buildout`_ to manage your instance installing 
ECLecture is very simple.  You can install it by adding it to the 
eggs line for your instance::

  [instance]
  eggs =
      ... 
      Products.ECLecture

After updating the configuration you need to run ``bin/buildout``, 
which will take care of updating your system.

Then restart your zope instance and use the Add/Remove products page
in Site Setup to install ECLecture.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Installing without buildout
---------------------------

Move (or symlink) the ``ECLecture`` folder of this project
(``Products.ECLecture/Products/ECLecture``) into the ``Products`` 
directory of the Zope instance it has to be installed for, and 
restart the server.  Use the Add/Remove products page in Site 
Setup to install ECLecture.


Support
=======

For questions and discussions about ECLecture, please join the
`eduComponents mailing list`_.

.. _eduComponents mailing list: https://listserv.uni-magdeburg.de/mailman/listinfo/educomponents


Credits
=======

ECLecture was written by `Mario Amelung`_ and `Michael Piotrowski`_.

The icons used in ECLecture are from the `Silk icon set`_ by Mark 
James.  They are licensed under a `Creative Commons Attribution 
2.5 License`_.

ECLecture was ported to Plone 3 and 4 by `Eudemonia Solutions AG`_ 
with support from `Katrin Krieger`_ and the Otto-von-Guericke 
University of Magdeburg.

.. _Mario Amelung: mario.amelung@gmx.de
.. _Michael Piotrowski: mxp@dynalabs.de
.. _Silk icon set: http://www.famfamfam.com/lab/icons/silk/
.. _Creative Commons Attribution 2.5 License: http://creativecommons.org/licenses/by/2.5/
.. _Eudemonia Solutions AG: http://www.eudemonia-solutions.de/
.. _Katrin Krieger: http://wdok.cs.uni-magdeburg.de/Members/kkrieger/
