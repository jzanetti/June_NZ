Data
=====

**JUNE_NZ** requires a number of input files, all the files below can be created by :doc:`link <Data_creation>`


Population data (demography)
^^^^^^^^^^^^^^^^^^^^

It defines the population (agents) to be used in the model.

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Population/demography data
   :file: data/data_population.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

.. note::

   ``The number of people (grouped by age)`` will determine the number of total people to be used in the model.

Geography data
^^^^^^^^^^^^^^^^^^^^

It defines the geography (grid) to be used in the model.

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Population/demography data
   :file: data/data_geography.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

Group (activities) data
^^^^^^^^^^^^^^^^^^^^

Group data contains different types of activities that an individual might do every day.

Commute
********

Commute defines how people move across different areas

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Population/commute data
   :file: data/data_commute.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1