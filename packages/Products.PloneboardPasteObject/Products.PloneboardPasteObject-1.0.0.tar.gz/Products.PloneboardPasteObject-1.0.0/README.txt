Introduction
============

This product is a fix for a behavior of Ploneboard that not allow to paste objects into archetypes 
Forum and into archetypes Conversation.
This behavior happens because the archetypes are implemented the INonStructuralFolder interface. 
To make possible the paste action into Ploneboard's types we fix the browser view named plone_context_state.
We have deleted the control that perform the check on the INonStructuralFolder into the function that identify 
the folder where we want to paste.
The delete of the check has made visible the add menu.
We have also fixed this problem. 
We had redefine the adapter named plone.contentmenu.factories for the archetypes Forum and Conversation.

