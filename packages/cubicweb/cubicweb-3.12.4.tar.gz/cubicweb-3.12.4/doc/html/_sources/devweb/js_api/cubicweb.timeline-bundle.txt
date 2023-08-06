===========================
cubicweb.timeline-bundle.js
===========================
.. module:: cubicweb.timeline-bundle.js

Append into urls each string in suffixes after prefixing it with urlPrefix.
@param {Array} urls
@param {String} urlPrefix
@param {Array} suffixes

Parse out the query parameters from a URL
@param {String} url    the url to parse, or location.href if undefined
@param {Object} to     optional object to extend with the parameters
@param {Object} types  optional object mapping keys to value types
       (String, Number, Boolean or Array, String by default)
@return a key/value Object whose keys are the query parameter names
@type Object

@fileOverview XmlHttp utility functions
@name SimileAjax.XmlHttp

Callback for XMLHttp onRequestStateChange.

Creates an XMLHttpRequest object. On the first run, this
 function creates a platform-specific function for
 instantiating an XMLHttpRequest object and then replaces
 itself with that function.

Performs an asynchronous HTTP GET.

@param {Function} fError a function of the form
     function(statusText, statusCode, xmlhttp)
@param {Function} fDone a function of the form function(xmlhttp)

Performs an asynchronous HTTP POST.

@param {Function} fError a function of the form
     function(statusText, statusCode, xmlhttp)
@param {Function} fDone a function of the form function(xmlhttp)

@fileOverview Graphics utility functions and constants
@name SimileAjax.Graphics

A boolean value indicating whether PNG translucency is supported on the
user's browser or not.

@type Boolean

Creates a DOM element for an <code>img</code> tag using the URL given. This
is a convenience method that automatically includes the necessary CSS to
allow for translucency, even on IE.

@function
@param {String} url the URL to the image
@param {String} verticalAlign the CSS value for the image's vertical-align
@return {Element} a DOM element containing the <code>img</code> tag

Creates an HTML string for an <code>img</code> tag using the URL given.
This is a convenience method that automatically includes the necessary CSS
to allow for translucency, even on IE.

@function
@param {String} url the URL to the image
@param {String} verticalAlign the CSS value for the image's vertical-align
@return {String} a string containing the <code>img</code> tag

Sets the opacity on the given DOM element.

@param {Element} elmt the DOM element to set the opacity on
@param {Number} opacity an integer from 0 to 100 specifying the opacity

Creates a nice, rounded bubble popup with the given content in a div,
page coordinates and a suggested width. The bubble will point to the
location on the page as described by pageX and pageY.  All measurements
should be given in pixels.

@param {Element} the content div
@param {Number} pageX the x coordinate of the point to point to
@param {Number} pageY the y coordinate of the point to point to
@param {Number} contentWidth a suggested width of the content
@param {String} orientation a string ("top", "bottom", "left", or "right")
  that describes the orientation of the arrow on the bubble
@param {Number} maxHeight. Add a scrollbar div if bubble would be too tall.
  Default of 0 or null means no maximum

Creates a nice, rounded bubble popup with the given page coordinates and
content dimensions.  The bubble will point to the location on the page
as described by pageX and pageY.  All measurements should be given in
pixels.

@param {Number} pageX the x coordinate of the point to point to
@param {Number} pageY the y coordinate of the point to point to
@param {Number} contentWidth the width of the content box in the bubble
@param {Number} contentHeight the height of the content box in the bubble
@param {String} orientation a string ("top", "bottom", "left", or "right")
  that describes the orientation of the arrow on the bubble
@return {Element} a DOM element for the newly created bubble

Creates a floating, rounded message bubble in the center of the window for
displaying modal information, e.g. "Loading..."

@param {Document} doc the root document for the page to render on
@param {Object} an object with two properties, contentDiv and containerDiv,
  consisting of the newly created DOM elements

Creates an animation for a function, and an interval of values.  The word
"animation" here is used in the sense of repeatedly calling a function with
a current value from within an interval, and a delta value.

@param {Function} f a function to be called every 50 milliseconds throughout
  the animation duration, of the form f(current, delta), where current is
  the current value within the range and delta is the current change.
@param {Number} from a starting value
@param {Number} to an ending value
@param {Number} duration the duration of the animation in milliseconds
@param {Function} [cont] an optional function that is called at the end of
  the animation, i.e. a continuation.
@return {SimileAjax.Graphics._Animation} a new animation object

Runs this animation.

Increments this animation by one step, and then continues the animation with
<code>run()</code>.

Creates a button and textarea for displaying structured data and copying it
to the clipboard.  The data is dynamically generated by the given
createDataFunction parameter.

@param {String} image an image URL to use as the background for the
  generated box
@param {Number} width the width in pixels of the generated box
@param {Number} height the height in pixels of the generated box
@param {Function} createDataFunction a function that is called with no
  arguments to generate the structured data
@return a new DOM element

@fileOverview A collection of date/time utility functions
@name SimileAjax.DateTime

An array of unit lengths, expressed in milliseconds, of various lengths of
time.  The array indices are predefined and stored as properties of the
SimileAjax.DateTime object, e.g. SimileAjax.DateTime.YEAR.
@type Array

Takes a date object and a string containing an ISO 8601 date and sets the
the date using information parsed from the string.  Note that this method
does not parse any time information.

@param {Date} dateObject the date object to modify
@param {String} string an ISO 8601 string to parse
@return {Date} the modified date object

Takes a date object and a string containing an ISO 8601 time and sets the
the time using information parsed from the string.  Note that this method
does not parse any date information.

@param {Date} dateObject the date object to modify
@param {String} string an ISO 8601 string to parse
@return {Date} the modified date object

The timezone offset in minutes in the user's browser.
@type Number

Takes a date object and a string containing an ISO 8601 date and time and
sets the date object using information parsed from the string.

@param {Date} dateObject the date object to modify
@param {String} string an ISO 8601 string to parse
@return {Date} the modified date object

Takes a string containing an ISO 8601 date and returns a newly instantiated
date object with the parsed date and time information from the string.

@param {String} string an ISO 8601 string to parse
@return {Date} a new date object created from the string

Takes a string containing a Gregorian date and time and returns a newly
instantiated date object with the parsed date and time information from the
string.  If the param is actually an instance of Date instead of a string,
simply returns the given date instead.

@param {Object} o an object, to either return or parse as a string
@return {Date} the date object

Rounds date objects down to the nearest interval or multiple of an interval.
This method modifies the given date object, converting it to the given
timezone if specified.

@param {Date} date the date object to round
@param {Number} intervalUnit a constant, integer index specifying an
  interval, e.g. SimileAjax.DateTime.HOUR
@param {Number} timeZone a timezone shift, given in hours
@param {Number} multiple a multiple of the interval to round by
@param {Number} firstDayOfWeek an integer specifying the first day of the
  week, 0 corresponds to Sunday, 1 to Monday, etc.

Rounds date objects up to the nearest interval or multiple of an interval.
This method modifies the given date object, converting it to the given
timezone if specified.

@param {Date} date the date object to round
@param {Number} intervalUnit a constant, integer index specifying an
  interval, e.g. SimileAjax.DateTime.HOUR
@param {Number} timeZone a timezone shift, given in hours
@param {Number} multiple a multiple of the interval to round by
@param {Number} firstDayOfWeek an integer specifying the first day of the
  week, 0 corresponds to Sunday, 1 to Monday, etc.
@see SimileAjax.DateTime.roundDownToInterval

Increments a date object by a specified interval, taking into
consideration the timezone.

@param {Date} date the date object to increment
@param {Number} intervalUnit a constant, integer index specifying an
  interval, e.g. SimileAjax.DateTime.HOUR
@param {Number} timeZone the timezone offset in hours

Returns a new date object with the given time offset removed.

@param {Date} date the starting date
@param {Number} timeZone a timezone specified in an hour offset to remove
@return {Date} a new date object with the offset removed

Returns the timezone of the user's browser.

@return {Number} the timezone in the user's locale in hours

A basic set (in the mathematical sense) data structure

@constructor
@param {Array or SimileAjax.Set} [a] an initial collection

Adds the given object to this set, assuming there it does not already exist

@param {Object} o the object to add
@return {Boolean} true if the object was added, false if not

Adds each element in the given set to this set

@param {SimileAjax.Set} set the set of elements to add

Removes the given element from this set

@param {Object} o the object to remove
@return {Boolean} true if the object was successfully removed,
  false otherwise

Removes the elements in this set that correspond to the elements in the
given set

@param {SimileAjax.Set} set the set of elements to remove

Removes all elements in this set that are not present in the given set, i.e.
modifies this set to the intersection of the two sets

@param {SimileAjax.Set} set the set to intersect

Returns whether or not the given element exists in this set

@param {SimileAjax.Set} o the object to test for
@return {Boolean} true if the object is present, false otherwise

Returns the number of elements in this set

@return {Number} the number of elements in this set

Returns the elements of this set as an array

@return {Array} a new array containing the elements of this set

Iterates through the elements of this set, order unspecified, executing the
given function on each element until the function returns true

@param {Function} f a function of form f(element)

A sorted array data structure

@constructor

@fileOverview UI layers and window-wide dragging
@name SimileAjax.WindowManager

This is a singleton that keeps track of UI layers (modal and
 modeless) and enables/disables UI elements based on which layers
 they belong to. It also provides window-wide dragging
 implementation.