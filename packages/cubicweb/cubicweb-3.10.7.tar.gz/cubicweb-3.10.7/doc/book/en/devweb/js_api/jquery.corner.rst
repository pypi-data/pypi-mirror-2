================
jquery.corner.js
================
.. module:: jquery.corner.js

The corner() method provides a simple way of styling DOM elements.  

corner() takes a single string argument:  $().corner("effect corners width")

  effect:  The name of the effect to apply, such as round or bevel. 
           If you don't specify an effect, rounding is used.

  corners: The corners can be one or more of top, bottom, tr, tl, br, or bl. 
           By default, all four corners are adorned. 

  width:   The width specifies the width of the effect; in the case of rounded corners this 
           will be the radius of the width. 
           Specify this value using the px suffix such as 10px, and yes it must be pixels.

For more details see: http://methvin.com/jquery/jq-corner.html
For a full demo see:  http://malsup.com/jquery/corner/


@example $('.adorn').corner();
@desc Create round, 10px corners 

@example $('.adorn').corner("25px");
@desc Create round, 25px corners 

@example $('.adorn').corner("notch bottom");
@desc Create notched, 10px corners on bottom only

@example $('.adorn').corner("tr dog 25px");
@desc Create dogeared, 25px corner on the top-right corner only

@example $('.adorn').corner("round 8px").parent().css('padding', '4px').corner("round 10px");
@desc Create a rounded border effect by styling both the element and its parent

@name corner
@type jQuery
@param String options Options which control the corner style
@cat Plugins/Corner
@return jQuery
@author Dave Methvin (dave.methvin@gmail.com)
@author Mike Alsup (malsup@gmail.com)