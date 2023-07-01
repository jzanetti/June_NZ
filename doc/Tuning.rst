Model tuning
=====

This page gives several examples about how to tune the model output towards observation.

The base example is given using the COVID-19 configuration of **JUNE**, the following parameters may be tuned:

- The number of people travel across super areas (e.g., ``group/commute/workplace_and_home.csv``).
- Infection outcome (e.g., ``disease/infection_outcome.csv``)


The experiments used to demostrate the tuning of model are described below:

.. tabularcolumns:: |p{5cm}|p{7cm}|p{4cm}|

.. csv-table:: Tuning information
   :file: data/tuning_exp.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1



**********
Base example
**********
The base example is used to show the model outputs without any tuning. 
The following figures are the model outputs for the Area of 51150 and 51440.

|pic1| |pic2|

|pic3| |pic4|

.. |pic1| image:: data/tuning/base/51150_infection_1.png
   :width: 45%

.. |pic2| image:: data/tuning/base/51150_infection_2.png
   :width: 45%

.. |pic3| image:: data/tuning/base/51440_infection_1.png
   :width: 45%

.. |pic4| image:: data/tuning/base/51440_infection_2.png
   :width: 45%


For 51150, we observe that the hospitalization rate was below 0.4%, indicating a relatively low proportion of individuals requiring hospital care. Conversely, the mortality rate stood at approximately 0.1%, suggesting a comparatively smaller percentage of individuals succumbing to the condition.
It takes a while (e.g., 15 days) until we see the first hospital case in the Area 51440.


**********
Increase the people is hospitalized and died
**********
The number of people who died, were hospitalized, and placed into ICU can be increased by using the following configuration:

.. code-block:: python

   infection_outcome:
   adjust_factor:
      "18-65": # age range
         gp: # population type
         male: # sex
            asymptomatic: 1.0
            mild: 1.0
            hospital: 10.0
            icu: 10.0
            home_ifr: 10.0
            hospital_ifr: 10.0
            icu_ifr: 10.0
         female: # sex
            asymptomatic: 1.0
            mild: 1.0
            hospital: 10.0
            icu: 10.0
            home_ifr: 10.0
            hospital_ifr: 10.0
            icu_ifr: 10.0


|pic5| |pic6|

|pic7| |pic8|

.. |pic5| image:: data/tuning/exp1/51150_infection_1.png
   :width: 45%

.. |pic6| image:: data/tuning/exp1/51150_infection_2.png
   :width: 45%

.. |pic7| image:: data/tuning/exp1/51440_infection_1.png
   :width: 45%

.. |pic8| image:: data/tuning/exp1/51440_infection_2.png
   :width: 45%


In the case of 51150, there has been a significant increase in hospitalizations, 
rising from 0.4% to 8.0%. Similarly, the proportion of individuals requiring intensive care unit (ICU) treatment has increased 
from approximately 0.1% to 1-2%. Unfortunately, the mortality rate has also seen a rise, escalating from 0.1% to 1-2%.