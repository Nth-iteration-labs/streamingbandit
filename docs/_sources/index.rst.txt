Welcome to StreamingBandit's documentation!
===========================================

Although the first version is released, the documentation and the code is 
still under development.
For any information contact the authors.

Documentation:

.. toctree::

   Core API <core> 
   Statistics API <stats>
   Evaluation API <eval>
   Admin API <admin>
   Management API <management>
   Libs <libs>
   Experiment <exp>

Contributing to the libraries
=============================

We gladly accept any contribution to expanding the libraries of
StreamingBandit.
The libraries that are currently written are all tested and have an agent that
functions with them.
If you would like to contribute by writing a part of the library, look at the
following points:

- Write a Base class according to the skeleton class __strmBase.
- Write a default example of a use-case of the class in the defaults folder.
- Write an agent in the utils folder that uses the class and the default
  example.

Changelog
=========
+------------+---------+------------------------------------------------------+
| Date       | Version | Changelog                                            |
+============+=========+======================================================+
| 01-12-2015 | v1      | First version made available.                        |
+------------+---------+------------------------------------------------------+
| 21-10-2016 | v2      | Second version made available.                       |
|            |         | Added classes, such as LiF, BTS, TBL.                |
+------------+---------+------------------------------------------------------+

Authors
=======

Maurits Kaptein (``maurits at mauritskaptein dot com``)

Jules Kruijswijk (``juleskruijswijk at gmail dot com``)
