=====================
jquery.tablesorter.js
=====================
.. module:: jquery.tablesorter.js

@description Create a sortable table with multi-column sorting capabilitys

@example $('table').tablesorter();
@desc Create a simple tablesorter interface.

@example $('table').tablesorter({ sortList:[[0,0],[1,0]] });
@desc Create a tablesorter interface and sort on the first and secound column in ascending order.

@example $('table').tablesorter({ headers: { 0: { sorter: false}, 1: {sorter: false} } });
@desc Create a tablesorter interface and disableing the first and secound column headers.

@example $('table').tablesorter({ 0: {sorter:"integer"}, 1: {sorter:"currency"} });
@desc Create a tablesorter interface and set a column parser for the first and secound column.


@param Object settings An object literal containing key/value pairs to provide optional settings.

@option String cssHeader (optional) 			A string of the class name to be appended to sortable tr elements in the thead of the table.
												Default value: "header"

@option String cssAsc (optional) 			A string of the class name to be appended to sortable tr elements in the thead on a ascending sort.
												Default value: "headerSortUp"

@option String cssDesc (optional) 			A string of the class name to be appended to sortable tr elements in the thead on a descending sort.
												Default value: "headerSortDown"

@option String sortInitialOrder (optional) 	A string of the inital sorting order can be asc or desc.
												Default value: "asc"

@option String sortMultisortKey (optional) 	A string of the multi-column sort key.
												Default value: "shiftKey"

@option String textExtraction (optional) 	A string of the text-extraction method to use.
												For complex html structures inside td cell set this option to "complex",
												on large tables the complex option can be slow.
												Default value: "simple"

@option Object headers (optional) 			An array containing the forces sorting rules.
												This option let's you specify a default sorting rule.
												Default value: null

@option Array sortList (optional) 			An array containing the forces sorting rules.
												This option let's you specify a default sorting rule.
												Default value: null

@option Array sortForce (optional) 			An array containing forced sorting rules.
												This option let's you specify a default sorting rule, which is prepended to user-selected rules.
												Default value: null

@option Array sortAppend (optional) 			An array containing forced sorting rules.
												This option let's you specify a default sorting rule, which is appended to user-selected rules.
												Default value: null

@option Boolean widthFixed (optional) 		Boolean flag indicating if tablesorter should apply fixed widths to the table columns.
												This is usefull when using the pager companion plugin.
												This options requires the dimension jquery plugin.
												Default value: false

@option Boolean cancelSelection (optional) 	Boolean flag indicating if tablesorter should cancel selection of the table headers text.
												Default value: true

@option Boolean debug (optional) 			Boolean flag indicating if tablesorter should display debuging information usefull for development.

@type jQuery

@name tablesorter

@cat Plugins/Tablesorter

@author Christian Bach/christian.bach@polyester.se

Add the table data to main data array