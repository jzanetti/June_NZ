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

``Comorbidities`` are defined by the variable ``FIXED_DATA``, which is located in ``process/__init__.py``. The comorbidity is one of the parameters determing the severity of symptom that
an individual may experience.

- ``comorbidities_female``: the ratio of female have certain comorbidities (grouped by ages)
- ``comorbidities_male``: the ratio of male have certain comorbidities (grouped by ages)
- ``comorbidities_intensity``: the intensity of the comorbidities

.. note::

    For example, if the average female comorbidity intensity for the age group 50 is ``1.02``: tt is caculated by ``[0, 0.1, 0.9] * [0.8, 1.2, 1.0]`` where ``[0, 0.1, 0.9]`` is the 
    ratio of comorbidities and ``[0.8, 1.2, 1.0]`` represents the intensities of comorbidities. 
        
    If a person has disease2, which has the intensity of ``1.2``, then the symptom multiplier factor for this person is ``1.2/1.02=1.18`` which is larger than 1.0, 
    and therefore will lead to higher chance of experiencing severe symptoms.

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
The transmssion profile determins the probability of the infection (e.g, the higher the probabilities, the more infectiousness an infector can be). 

The probability of the infection is usually chosen from a ``Gamma`` profile, which is defined by ``(shape,shift,scale)``. 
The following figures show the ``Gamma`` profile for different ``shape``, ``shift (loc)`` and ``scale``. 
The x-axis is the value of ``shift (loc)``, which corresponds to the infection time. The y-axis is the probability of infection.

.. image:: data/gamma_profile.jpg
   :scale: 50 %
   :alt: Gamma profile
   :align: center

When a person is infected, the infection time will be applied to the above ``Gamma`` function (as ``x``), and then obtain the related probability of infection. 

For example, for ``COVID-19``, the following transmission profile is set up:

.. code-block:: python

        type:
                'gamma'
        shape:
                type: normal 
                loc: 1.56
                scale: 0.08
        rate:
                type: normal 
                loc: 0.53
                scale: 0.03
        shift:
                type: normal 
                loc: -2.12
                scale: 0.1
        asymptomatic_infectious_factor:
                type: constant
                value: 0.5
        mild_infectious_factor:
                type: constant
                value: 1.
        max_infectiousness:
                type: lognormal
                s: 0.5 
                loc: 0.0
                scale: 1. 


