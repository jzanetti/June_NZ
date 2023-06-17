Creating data for JUNE_NZ
=====

The script ``cli_data.py`` is provided to create all the required inputs for **JUNE_NZ**.

.. code-block:: console

    cli_data --workdir /tmp/nz --cfg etc/june_data.yml --scale 0.1 [--exclude_super_areas A1, A2]

The command options are explained as below:

- ``--workdir``: Specifies the directory where the generated data will be stored.
- ``--cfg``: Sets the configuration for retrieving the source data.
- ``--scale``: Determines the percentage of the population to be used. For instance, a value of 0.1 means only 10% of the population will be utilized.
- ``--exclude_super_areas``: Allows excluding specific super areas from the model.

There are two types of output from ``cli_data.py``:

- ``data``: the data to be used in **JUNE_NZ**
- ``configuration``: the configuration to be used in **JUNE_NZ**

Configuration
********

``cli_data`` creates the following configurations:

- ``comorbidities``


Most configurations are defined by the variable ``FIXED_DATA``, which is located in ``process/__init__.py``

- ``comorbidities``: the co-morbidities are defined in ``demography`` -> ``comorbidities_female`` / ``comorbidities_male``:

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
                }
                ...
            }