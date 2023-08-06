Solgema.fullcalendar Package Readme
=========================

Overview
--------

Solgema.fullcalendar is a complete implementation of Adam Shaw Fullcalendar into Plone.
More info on Fullcalendar here: http://arshaw.com/fullcalendar/

This calendar allows you to display events type objects in a powerfull and fast ajax agenda.
You will be also able to add, edit and more generally manage your events throught the Calendar
with a strong AJAX framework.

The calendar is a view you can choose on a Topic. The view is named "solgemafullcalendar_view".
After that, a new object action permits you to set up the basics parameters for the calendar.

The calendar is strongly linked to the Topic as the events it displays are searched by the Topic and
it's criterias.

In addition to the calendar, there is a small query form you can display in the bottom of
the calendar to choose which event you want to display. The fields in this query form are
taken from the Topic's Criterions.


Changelog for Solgema.fullcalendar
--------
*Solgema.fullcalendar 1.0

 -Added relative start hour and relative start day
 -Fixed paste action in contextual content menu (when nothing in clipboard)
 -Fixed error when deleting topic's criterion after having set them in calendar view criterias.
 -Several bug fixed


*Solgema.fullcalendar 0.3

 -Added automatic dependencies installation in install.py ( installation of Solgema.ContextualContentMenu )
 -Changed the javascript in SFAjax_base_edit.cpt so that when editing through calendar, the dialog's iframe
  is resized to display the entire edit form ( fixes issue #1 )
 -Changed Dialog title when adding content ( msgid was "label_add_type" in Plone 3 and now 'heading_add_item'
  in Plone 4 ).


*Solgema.fullcalendar 0.2

 -Added a topicRelativeUrl variable into solgemafullcalendar_vars to fix the cookies path.
  (fix an issue with mutiple cookies when the topic is default view of a folder)
