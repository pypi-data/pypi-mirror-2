.. _mask:

=========
 SqlMask
=========

.. image:: ../img/mask-demo.png
   :align: right
   :scale: 50%
   :class: preview

.. autoclass:: sqlkit.widgets.SqlMask()
   :members: get_widget, clear_mask, set_frame_label

Introspection of the table is used to determine which widgets will be used to
edit the data. The following rules are applied:

  :varchar: gtk.Entry
     
  :numbers: gtk.Entry with right alignment

  :bool: gtk.CheckBox

  :text: gtk.Text
  
  :FKey: fk_edit (a custom ComboBoxEntry)

  :date/datetime: dateedit (entry + arrow for calendar + time)

  :default: gtk.Entry

All fields will have a label that is sensitive to mouse clicks. A mouse
click pops up a :ref:`filter <filters>` widget.

layout
=======

The most powerful part of SqlMask is the ability to define the layout via
simple text description. In the examples you'll see how easy it is to create
fancy layout that have all nice gtk Widgets like expanders, notebooks, panes
and it makes it incredibly easy to nest SqlTables into SqlMask to build
complex layout that represent also :ref:`relationships`.

If no layout is provided a flat one will be generated on the fly.

.. image:: ../img/layout-simple.png
   :align: right

The key is that a textual layout is parsed to see if the token are
recognized as fields of the table that the mask is editing, in which case
introspection is done to understand which widget should be used to edit the
data (according to rules above) and a label is added::

   title
   date_release
   L=description TXS=description
   director_id

will show a mask with an entry, a date a text and a fkey. Title and
director_id will be already instrumented with completion: director_id will
try to complete choosing the values of directors from the director table,
title will suggest completion based on title present in the table (and in
this case may not be very useful). Description would render is am entry as
it's a varchar, we wanted to "cast" it to text so we had to explicitly add
also a token for the label. L is the identified for a sensitive label (a
gtk.Label inside a gtk.Event) and TX is the identifier or a scrolled text.

The description language you can use is petty rich (and dynamic, so you can
add your custom made widgets): you'd better have  a look at the demo of
sqlkit.layout that you find in sqlkit.demo.layout

When parsing the textual layout, any token that is not recognized as a
field is passed as is to ``sqlkit.layout.Layout`` 


gtk refinements
---------------

Occasionally you may need to refine your layout, change packing, visibility,
attribute an so on. You can reach the gtk widgets via the ``widgets``
attribute of the SqlWidget. In example 26 we use::

  Tbl = t.widgets['T.a']
  Tbl.get_parent().child_set_property(Tbl, 'y-options', gtk.EXPAND|gtk.FILL)

that changes pack properties to a gtk.Table whose name is ``T.a``


Shortcuts
----------


:mouse scrolling: allows to browse the records that have been loaded by a
   reload operation
:Control-s:  saves the record
:Control-q:  quits the table
:Control-n:  opens a new record

Signals
========

:pre-display: 

     this signal is emitted when current object has already been set but
     field values have no been set. It can be used to configure custom
     widgets whose appearance may depend on other values.

  .. method:: pre_display_cb(mask, obj)
 
     :param mask: the SqlMask that emitted the signal
     :param obj: the object currently selected or None

.. versionadded:: 0.8.8

