==================
cubicweb.compat.js
==================
.. module:: cubicweb.compat.js

.. function:: cw.utils.deprecatedFunction(msg, function)

jQUery flattens arrays returned by the mapping function:
>>> y = ['a:b:c', 'd:e']
>>> jQuery.map(y, function(y) { return y.split(':');})
["a", "b", "c", "d", "e"]
 // where one would expect:
 [ ["a", "b", "c"], ["d", "e"] ]
 XXX why not the same argument order as $.map and forEach ?

The only known usage of KEYS is in the tag cube. Once cubicweb-tag 1.7.0 is out,
this current definition can be removed.