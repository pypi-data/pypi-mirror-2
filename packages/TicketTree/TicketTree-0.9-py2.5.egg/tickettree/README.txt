Ticket Tree for Trac

  Copyright 2010 Roberto Longobardi, Marco Cipriani

  Project web page on TracHacks: http://trac-hacks.org/wiki/TicketTree
  
  Project web page on SourceForge.net: http://sourceforge.net/projects/tickettree4trac/
  
  Project web page on Pypi: http://pypi.python.org/pypi/TicketTree


A Trac plugin to display tickets in a tree, organized based on structured ticket titles.


More details:

Often struggled with thousands of Trac tickets and missing a clear picture of where the problems are?

Ticket Tree allows you to categorize your tickets based on the areas affected. 
Given this categorization, you can then display the tickets in a tree, getting a better picture 
of the areas and sub-areas with more problems.
In addition to that, the tree view lets you navigate your tickets more easily.

The categorization mechanism is really simple, as it's based on the ticket title.
You will use the dash '-' character to define the category and sub-categories in your tickets.

For example, giving the following title to a ticket:

 User Interface - Main menu - File menu - Unable to click on the "Open File" item

will display your ticket in the tree as follows:

 + User Interface 
   + Main menu 
     + File menu
         Unable to click on the "Open File" item


=== Statistics: ===
Next to each category you will see the number of all tickets, and the detail of open and 
closed tickets, in that category.

=== Searching and Filtering: ===
You can quickly search and filter tickets in the tree using the "Find" text box.
Just start typing text in it to see your ticket tree reducing and highlighting only the tickets
matching your text.
You can type more than one word: only the tickets matching all of them will be displayed.
Special words are "open" and "closed": they will limit the view to only open and closed tickets,
respectively.

=== Querying: ===
The plugin provides a macro, which lets you build custom ticket trees based on specific ticket 
queries.
Used without any parameter, the macro will display a tree with all of the tickets.

=== Simplified categorization: ===
An interesting feature is the ability to open a ticket in a specific category directly from the 
tree. 
Next to each category you'll find a "new" link, clicking which you will be opened the ticket 
creation page with the ticket's title already built with the corresponding category and 
sub-categories, and a place-holder for the ticket's short description to follow.

=== Refreshing: ===
The "Refresh" butto is useful to perform the query again and update the tree.


=================================================================================================  
Change History:

(Refer to the tickets on trac-hacks for complete descriptions.)

Release 0.9 (2011-06-01):
  o First release publicly available.
