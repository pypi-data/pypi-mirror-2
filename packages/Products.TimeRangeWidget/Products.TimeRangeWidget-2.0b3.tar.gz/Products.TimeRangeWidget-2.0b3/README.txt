Introduction
============

Provides an archetypes field which stores a time range (from, to) 
in a string field.

Example
-------

::

    from Products.TimeRangeWidget.widget import TimeRangeWidget
    
      ...
    
    StringField('timerange',
        widget = TimeRangeWidget(
            description = '',
            label = _at(u'label_timerange', default=u'Time range'),
            size = 40
        )
    ),
    
      ...

