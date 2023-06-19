##############
Data
##############

**JUNE_NZ** requires a number of input files.

The script ``cli_data.py`` is provided to create all the required inputs for **JUNE_NZ**.

.. code-block:: console

    cli_data --workdir <Working directory> 
             --cfg <Data configuration> 
             --scale <Population scale> 
             --disease_cfg_dir <Disease configuration directory>
             --policy_cfg_path <Policy configuration path>
             [--exclude_super_areas A1, A2]

The command options are explained as below:

- ``--workdir``: Specifies the directory where the generated data will be stored. For example, ``--workdir /tmp/june_data``.
- ``--cfg``: Sets the configuration for retrieving the source data. For example, ``--cfg etc/june_data.yml``.
- ``--scale``: Determines the percentage of the population to be used. For instance, a value of 0.1 means only 10% of the population will be utilized. For example, ``--scale 0.1``
- ``--exclude_super_areas``: Allows excluding specific super areas from the model. For example, ``--exclude_super_areas A1 A2``.
- ``--disease_cfg_dir``: Disease configuration directory. For example, ``--disease_cfg_dir etc/cfg/disease/covid-19``.
- ``--policy_cfg_path``: Policy file. For example, ``--policy_cfg_path etc/cfg/policy/policy1.yaml``.
- ``--simulation_cfg_path``: Simulation file. For example, ``--simulation_cfg_path etc/cfg/simulation/simulation_cfg.yml``.

The following contents show different types of inputs for **JUNE_NZ**.

**********
1. Population data (demography)
**********

It defines the population (agents) to be used in the model.

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Population/demography data
   :file: data/data_population.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

.. note::

   ``The number of people (grouped by age)`` will determine the number of total people to be used in the model.

**********
2. Geography data
**********

It defines the geography (grid) to be used in the model.

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Geography data
   :file: data/data_geography.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

**********
3. Group (activities) data
**********

Group data contains different types of activities that an individual might do every day.

3.1 Company
===============
It defines the companies used in the model

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Company data
   :file: data/data_company.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

In the above data, ``Number of employers by firm size``, ``Number of employers by sector type`` and ``Number of employees``
are obtained from external dataset, while the ``company clousre`` and ``sub-sector configuration`` are defined in the variable ``FIXED_DATA``. For example,


.. code-block:: python

        "company": {
            "employees": {"employment_rate": 0.7},
            "company_closure": {
                "company_closure": {
                    "sectors": {
                        "A": {"key_worker": 1.0, "furlough": 0.0, "random": 0.0},
                        "P": {"key_worker": 0.0, "furlough": 0.0833, "random": 0.9167},
                        ...
                        "O": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "R": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "S": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                    }
                }
            },
            "subsector_cfg": {
                "age_range": [18, 64],
                "sub_sector_ratio": {"P": {"m": 0.4, "f": 0.6}, "Q": {"m": 0.5, "f": 0.5}},
                "sub_sector_distr": {
                    "P": {
                        "label": ["teacher_secondary", "teacher_primary"],
                        "m": [0.72526887, 0.27473113],
                        "f": [0.72526887, 0.27473113],
                    },
                    ...
                    "Q": {
                        "label": ["doctor", "nurse"],
                        "m": [0.65350126, 0.34649874],
                        "f": [0.16103136, 0.83896864],
                    },
                },
            },
        },


.. note::

        The ``Number of employees`` from NZStats somehome is smaller than the expected value compared to the NZ population. Therefore, in ``FIXED_DATA``
        we have a variable called ``employment_rate``, which is a factor makes the total ``number of employees`` matches to the assumed ``employment rate``.


3.2 Household
===============
It defines the household information used in the model

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Household data
   :file: data/data_household.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

The household information come from both external dataset and ``FIXED_DATA``:

For example, 

- for setting up the age differences between couples and parents-children, we have:

        .. code-block:: python

                FIXED_DATA = {
                    "group": {
                        ......
                        "household": {
                            "age_difference_couple": {
                                "age_difference": [-5, 0, 5, 10],
                                "frequency": [0.1, 0.7, 0.1, 0.1],
                            },
                            "age_difference_parent_child": {
                                "age_difference": [25, 50],
                                "0": [0.1, 0.9],
                                "1": [0.1, 0.9],
                                "2": [0.2, 0.8],
                                "3": [0.3, 0.7],
                                "4 or more": [0.3, 0.7],
                            },
                        },
                    ...

    where the above defines the assumed age differences.

- The ``number of household`` are obtained from NZStats, note that since there is a lack of detailed information, the only household type ``=0 >=0 >=0 >=0 >=0`` is used.

- We also set the number of commnual and student househodls to zero, since the lack of detailed dataset.

3.3 Hospital
===============
It defines the hospital information used in the model

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Hospital data
   :file: data/data_hospitals.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

The information would include the hospital address (latitude and longitude), number of beds and number of ICU beds. Also some meta data around it,
such as the the minimum age working in this sector, and how many hospitals that an indiviual could visit.


3.4 School
===============
It defines the school information used in the model

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: School data
   :file: data/data_schools.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

The information would include the school address (latitude and longitude), and the student profile (e.g., min and max age)


3.5 Leisure (cinema, grocery, pub and gym)
===============
It defines the leisure information used in the model

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: leisure data
   :file: data/data_leisures.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

The information would include all the leisure activities.

Note that all the location information are obtained from the Open Street Map, while all the configurations are from ``FIXED_DATA``. For example, for ``cinema``, we have:


.. code-block:: python


        "pub": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 0.032,
                            "9-15": 0.106,
                            "15-19": 0.126,
                            "19-31": 0.738,
                            "31-51": 0.421,
                            "51-66": 0.533,
                            "66-86": 0.15,
                            "86-100": 0.033,
                        },
                        "female": {
                            "0-9": 0.135,
                            "9-15": 0.147,
                            "15-19": 0.358,
                            "19-31": 0.544,
                            "31-51": 0.4,
                            "51-66": 0.409,
                            "66-86": 0.101,
                            "86-100": 0.02,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 0.038,
                            "9-15": 0.101,
                            "15-19": 0.106,
                            "19-31": 0.321,
                            "31-51": 0.262,
                            "51-66": 0.304,
                            "66-86": 0.176,
                            "86-100": 0.063,
                        },
                        "female": {
                            "0-9": 0.043,
                            "9-15": 0.081,
                            "15-19": 0.141,
                            "19-31": 0.251,
                            "31-51": 0.231,
                            "51-66": 0.18,
                            "66-86": 0.146,
                            "86-100": 0.06,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 11},
                        "female": {"0-65": 3, "65-100": 11},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "neighbours_to_consider": 7,
                "maximum_distance": 10,
            },
            
The above shows how frequent a person might visit a ``cinema`` (over weekdays and weekends), how many different cinemas he/she might consider, and how long
he/she might travel to go to a cinema.


**********
4. Commute
**********

Commute defines how people move across different areas

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Group/commute data
   :file: data/data_commute.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

Note that ``transport_def.yaml`` is defined in the variable ``FIXED_DATA``, e.g.,

.. code-block:: python

    FIXED_DATA = {
        ...
        "group": {
            "commute": {
                "transport_def": [
                    {"description": "Work mainly at or from home", "is_public": False},
                    {"description": "Underground, metro, light rail, tram", "is_public": True},
                    
                    ...

                    {"description": "On foot", "is_public": False},
                    {"description": "Other method of travel to work", "is_public": False},
                ]
            },
        ...


**********
5. Interaction
**********

It defines the interaction intensity matrix for all the group members (e.g., school, hospital etc.)

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: interaction data
   :file: data/data_interaction.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1

The above data are defined through ``FIXED_DATA``.


**********
6. Disease data
**********

Defines virus properties:

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Disease/Disease data
   :file: data/data_disease.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1


6.1 Comorbidities
============

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



6.2 Virus intensity
============

The virus intensity is a parameter that influences the severity of symptoms. 
As the intensity value increases, the likelihood of an individual experiencing more severe symptoms also increases. 
This can be achieved by elevating the probability of severe symptoms in addition to the 'infection_outcome' input data."

An example of the virus intensity is:

.. code-block:: python

        Covid19: 1.3 # 170852960
        B117: 1.5 # 37224668
        B16172: 1.5 # 76677444



6.3 Symptom trajectory (infection outcome)
============

For the symptom trajectory, it is defined by a set of distribution functions (e.g., beta, log-normal etc.). 
Each distribution function comes with a set of parameters, those parameters decide the timeline for different symptoms during the infection.

The considered symptom stages include:

- Recovered (-3)
- Healthy (-2)
- Exposed (-1)
- Asymptomatic (0)
- Mild (1)
- Severe (2), which is calculated by ``1.0 - [ Hospital + Die (from Home) + Asymptomatic + Mild]``
- Hospital (3)
- ICU (4)
- Die (from home, 5)
- Die (from hospital, 6)
- Die (from ICU, 7)

For example, if we need to create a symptom trajectory for ``Die (from hospital, 6)``, 
we need to go through the stages of ``Exposed (-1)``, ``Mild (1)``, ``Hospital (3)`` and ``Die (from hospital, 6)`` one by one. 
Among this trajectory, at the stage of ``mild (-1)``, we create samples from a ``log-normal`` distribution with a specific, predefined parameters 
(e.g., ``shape=0.55``, ``loc=0.0``, ``scale=5.0``), a random number is drawn from these samples, 
and it represents the timing for the infection (or we can understand it as the end time for the stage of symptom).

- The chance of having a symptom is determined by:

    - Comorbidities (see the Section 4.1 of comorbidities for details)
    - Input infection outcome statistics (e.g., the percentage of symptoms that a person may experience, see Sectoin 4.3.1)
    - The target virus intnsity (see Section 4.2)

- How long the sympton will last is dependant on:

    - The symptom trajectory (see Sectoin 4.3.2)

6.3.1 Input infection outcome statistics
---------

An example of the infection outcome statistics is:

.. tabularcolumns:: |p{5cm}|p{7cm}|p{7cm}|p{7cm}|

.. csv-table:: Disease/ infection outcome 
   :file: data/infection_outcome_ratio.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1 1


6.3.2 Symptom trajectory (infection outcome)
---------

An example of the symptom trajectory is:

.. code-block:: python

        # exposed => mild => hospitalised => dead
        - stages:
        - symptom_tag: exposed
                completion_time:
                type: beta
                a: 2.29
                b: 19.05
                loc: 0.39
                scale: 39.8

        - symptom_tag: mild
                completion_time:
                type: lognormal
                s: 0.55
                loc: 0.0
                scale: 5.

        - symptom_tag: hospitalised
                completion_time:
                type: beta
                a: 1.21
                b: 1.97
                loc: 0.08
                scale: 12.9      

        - symptom_tag: dead_hospital
                completion_time:
                type: constant
                value: 0.


6.4 Transmission profile
============

6.4.1 Base probability of infection
----------------
The transmssion profile determins the probability of the infection (e.g, the higher the probabilities, the more infectiousness an infector can be). 

The probability of the infection is usually chosen from a ``Gamma`` profile, which is defined by ``(shape,shift,scale)``. 
The following figures show the ``Gamma`` profile for different ``shape``, ``shift (loc)`` and ``scale``. 
The x-axis is the value of ``shift (loc)``, which corresponds to the infection time. The y-axis is the probability of infection.

.. image:: data/gamma_profile.png
   :scale: 100%
   :alt: Gamma profile
   :align: center

When a person is infected, the infection time will be applied to the above ``Gamma`` function (as ``x``), and then obtain the related probability of infection. 


6.4.2 Adjust max infectiousness
----------------

The maximum infectiousness from the probability of infection is adjusted with the argument ``max_infectiousness``. For an infector, a random
value will be drawn from the ``lognormal`` function, and it will be multiplied to the probability of function. 

The ``lognormal`` is determined by parameters of ``shape``, ``loc`` and ``scale``.
For example, the following figures show the ``lognormal`` profile:

.. image:: data/lognormal_profile.png
   :scale: 100%
   :alt: Lognormal profile
   :align: center

6.4.3 Adjust mild/asymptomatic infectiousness
----------------

We can adjust the the probability of infection based on a person's maximum symptom. For example, if the maximum symtom is ``asymptomatic``, we can
reduce the probability of infection profile by 50%.

An example for ``COVID-19`` transmission is set up as:

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