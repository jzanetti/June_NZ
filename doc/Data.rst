Data
=====

**JUNE_NZ** requires a number of input files, all the files below can be created by :doc:`link <Data_creation>`


1. Population data (demography)
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

2. Geography data
^^^^^^^^^^^^^^^^^^^^

It defines the geography (grid) to be used in the model.

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Geography data
   :file: data/data_geography.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

3. Group (activities) data
^^^^^^^^^^^^^^^^^^^^

Group data contains different types of activities that an individual might do every day.

3.1 Commute
********

Commute defines how people move across different areas

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Group/commute data
   :file: data/data_commute.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1


4. Disease data
^^^^^^^^^^^^^^^^^^^^

4.1 Comorbidities
************

``Comorbidities`` are defined by the variable ``FIXED_DATA``, which is located in ``process/__init__.py``. To understand Comorbidities in **JUNE_NZ**, please go to :doc:`link <comorbidities>`

An example of the defination of ``Comorbidities`` is:

.. code-block:: python

    FIXED_DATA = {
        ...

        "demography": {
            "comorbidities_female": {
                "comorbidity": ["disease1", "disease2", "no_condition"],
                5: [0, 0, 1.0],
                10: [0, 0, 1.0],
                20: [0, 0, 1.0],
                50: [0, 0.1, 0.9],
                75: [0, 0.2, 0.8],
                100: [0.9, 0.0, 0.1],
            },
            "comorbidities_male": {
                "comorbidity": ["disease1", "disease2", "no_condition"],
                5: [0, 0, 1.0],
                10: [0, 0, 1.0],
                20: [0, 0, 1.0],
                50: [0, 0.1, 0.9],
                75: [0, 0.2, 0.8],
                100: [0.9, 0.0, 0.1],
            },
            "comorbidities_intensity": {"disease1": 0.8, "disease2": 1.2, "no_condition": 1.0},
        }
        ...
    }



4.2 Transmission profile
************

