Introduction
============

Provides an archetypes field which stores a dimension (width, heigth) in a string field

Example
-------

::

    from Products.DimensionWidget.widget import DimensionWidget
    
      ...
    
    StringField('dimension',
        widget = DimensionWidget(
            description = '',
            label = _at(u'label_dimension', default=u'Dimension')
        )
    ),
    
      ...

