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
^^^^^^^^^^^^^^^^^^^^

``cli_data`` creates the following configurations:

- ``comorbidities``


Most configurations are defined by the variable ``FIXED_DATA``, which is located in ``process/__init__.py``

Comorbidities
*********

The co-morbidities (prevalence) are defined in ``demography`` -> ``comorbidities_female`` / ``comorbidities_male`` / ``comorbidities_intensity``, for example, 
the following configuration gives the age/gender dependant comorbidities (prevalence) of two diseases (disease1 and disease2) and no-condition:

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

.. note::

    ``comorbidity`` is used as one of the parameters for determining the susceptibility of an individual (together with the intensity, and the default susceptibility of target virus). 
    
    The prevalence of background diseases (comorbidity) for each age & gender group :math:`C_{i,(a,g)}` (:math:`i` means the comorbidity type, :math:`a` and :math:`g` represent age and gender group, respectively). The intensity of each background diseases is :math:`M_i` (:math:`i` means the comorbidity type). 

    So the accumulated intensity of the background disease at the age :math:`a` and for the gender :math:`g` , :math:`K_{(a,g)}'`, can be represented as:

        .. math::

            K_{(a,g)}' = \sum_{i=0}^N M_i C_{i, (a,g)}

    Where :math:`N` represents the total types of comorbidities (including “no-condition”).

    Given a person has the comorbidity of :math:`j`, the intensity of this comorbidity, therefore, is :math:`M_j`. So relative intensity for :math:`j` is:

        .. math::

            M_{j}' = \frac{M_j}{{K_{(a,g)}'}}

    When :math:`M_j > 1.0`, it means that this person is more likely to experience significant symptoms than average, while when :math:`M_j < 1.0`, this person is less likely to experience significant symptoms than average. 

    Details can be found ``june/epidemiology/infection/health_index/health_index.py``. In the function ``apply_effective_multiplier(self, probabilities, effective_multiplier)``,
    we have the probability of having severe symptoms as ``modified_probability_severe = probability_severe * effective_multiplier`` where 
    ``effective_multiplier`` is :math:`M_j`.