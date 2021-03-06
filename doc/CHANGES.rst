.. This file is a part of the AnyBlok / WMS Base project
..
..    Copyright (C) 2018 Georges Racinet <gracinet@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Release history
===============

0.6.0
~~~~~
* Published on PyPY
* Implemented Avatars
* Uniformisation of the relationship between Operations and Goods
  (Avatars)
* wms_reservation: initial implementation (with architectural notes in
  doc)
* some factorisation of concrete Operation methods into the base
  class, leading to much simpler implementations.

0.5
~~~
* First tag, not released to PyPI.
* Operations behave consistently; in particular stock levels at a
  given Location are consistent for all Goods states at any date and time.
* Initial Operations: Arrival, Departure, Move, Unpack, Split, Aggregate
