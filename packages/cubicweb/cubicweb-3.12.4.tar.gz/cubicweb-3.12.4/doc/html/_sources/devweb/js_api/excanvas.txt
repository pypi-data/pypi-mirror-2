===========
excanvas.js
===========
.. module:: excanvas.js

This funtion is assigned to the <canvas> elements as element.getContext().
@this {HTMLElement}
@return {CanvasRenderingContext2D_}

Binds a function to an object. The returned function will always use the
passed in {@code obj} as {@code this}.

Example:

  g = bind(f, obj, a, b)
  g(c, d) // will do f.call(obj, a, b, c, d)

@param {Function} f The function to bind the object to
@param {Object} obj The object that should act as this when the function
    is called
@param {*} var_args Rest arguments that will be used as the initial
    arguments when the function is called
@return {Function} A new function that has bound this

Public initializes a canvas element so that it can be used as canvas
element from now on. This is called automatically before the page is
loaded but if you are creating elements using createElement you need to
make sure this is called on the element.
@param {HTMLElement} el The canvas element to initialize.
@return {HTMLElement} the element that was created.

This class implements CanvasRenderingContext2D interface as described by
the WHATWG.
@param {HTMLElement} surfaceElement The element that the 2D context should
be associated with

@private

***** STUBS *******