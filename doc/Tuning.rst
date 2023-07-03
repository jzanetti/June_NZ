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
   enable: true
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


**********
Make people to be infected quicker
**********

Increase contact frequency
----------------------

The first apporach is that we can increase the contact frequency (:math:`beta`) in ``etc/data/realworld_auckland/interaction/general.yaml``:

.. code-block:: python

   contact_frequency_beta:
   enable: true
   adjust_factor:
      cinema: 10.0
      city_transport: 10.0
      company: 10.0
      grocery: 10.0
      gym: 10.0
      hospital: 10.0
      household: 10.0
      household_visits: 10.0
      inter_city_transport: 10.0
      pub: 10.0
      school: 10.0

As above, we increased the base contact frequency intensity by 10 times.

|pic9| |pic10|

|pic11| |pic12|

.. |pic9| image:: data/tuning/exp2/51150_infection_1.png
   :width: 45%

.. |pic10| image:: data/tuning/exp2/51150_infection_2.png
   :width: 45%

.. |pic11| image:: data/tuning/exp2/51440_infection_1.png
   :width: 45%

.. |pic12| image:: data/tuning/exp2/51440_infection_2.png
   :width: 45%

In comparison to the baseline experiment, a notable observation in Area 51150 is a higher rate of infection within the initial week. However, there haven't been significant alterations in terms of hospitalization and mortality rates since the infection outcomes configurations were not modified.

On the other hand, the impact of the experiment is particularly pronounced in Area 51440. Here, the rate of infection has significantly accelerated when compared to the baseline experiment.

Change probability of infection
----------------------

The probability of infection is determined by a ``Gamma`` function, which has three parameters: ``shape``, ``scale`` and ``shift``:

|pic13| |pic14|

|pic15| |pic16|

.. |pic13| image:: data/tuning/exp3/gamma_shift.png
   :width: 45%

.. |pic14| image:: data/tuning/exp3/gamma_shape.png
   :width: 45%

.. |pic15| image:: data/tuning/exp3/gamma_scale1.png
   :width: 45%

.. |pic16| image:: data/tuning/exp3/gamma_scale2.png
   :width: 45%

The probability of infection is considered from the moment a person is infected.

- The ``shift`` parameter determines the starting time of infection. Prior to the specified shift, the probability of infection is 0.0%.

- On the other hand, the ``shape`` parameter defines the shape of the ``Gamma`` function, which influences the rate at which infectiousness reaches its peak. A higher value for ``shape`` leads to a slower increase in infectiousness and a smoother probability curve over time.

- As for the ``scale`` parameter, increasing its value results in a smoother probability curve of infection over time.

It is challenging to adjust the probability of infection directly by modifying the ``Gamma`` function, for example, by merely increasing or decreasing the probability.

Moreover, we can adjust value of the infectiousness at its peak ~ ``max_infectiousness``, 
which is usually represented by a ``lognormal`` function. The ``lognormal`` is determined by three factors, ``shift``, ``loc`` and ``scale``:

|pic17| |pic18|

.. |pic17| image:: data/tuning/exp3/lognorm_scale.png
   :width: 45%

.. |pic18| image:: data/tuning/exp3/lognorm_shape.png
   :width: 45%

The final infection probability is calculated by ``max_infectiousness(t) * Gamma(t)``. In order to make the tuning simpler, we can use constant to represent ``max_infectiousness`` as well.

.. code-block:: python

   pobability_of_infection:
   enable: true
   adjust_factor:
      max_infectiousness:
        type: constant
        value: 10.0


|pic19| |pic20|

|pic21| |pic22|

.. |pic19| image:: data/tuning/exp3/51150_infection_1.png
   :width: 45%

.. |pic20| image:: data/tuning/exp3/51150_infection_2.png
   :width: 45%

.. |pic21| image:: data/tuning/exp3/51440_infection_1.png
   :width: 45%

.. |pic22| image:: data/tuning/exp3/51440_infection_2.png
   :width: 45%

In simpler terms, when we increased the frequency of interactions among individuals (represented by the contact matrix), we didn't observe significant changes in terms of hospitalization and mortality rates. This is because the outcomes of the infection were not modified.

However, it's important to note that in this experiment, the rate of exposure to the infection during the first 1-2 weeks was much higher compared to the baseline experiment.


Reduce the symptom cycle
----------------------

The period of people expericing a symptom is determined by the ``symptom_trajectory``. 

We usually have the following trajectories:

- exposed => asymptomatic => recovered
- exposed => mild => recovered 
- exposed => mild => severe => recovered
- exposed => mild => hospitalised => recovered
- exposed => mild => intensive_care => recovered
- exposed => mild => severe => dead
- exposed => mild => hospitalised => dead
- exposed => mild => hospitalised => intensive_care => dead

each stage of the symptom can be represented by different types of functions:

- ``beta`` (parameters: ``a``, ``b``, ``loc``, ``scale``)
- ``lognormal`` (parameters: ``shape``, ``loc``, ``scale``)
- ``exponweib`` (parameters: ``a``, ``c``, ``loc``, ``scale``)
- ``constant``

Now let's check individual probability functions:

- For ``beta`` (as below):

   - when we increase ``a``, the timing will increase
   - when we increase ``b``, the timing will decrease
   - when we increase ``scale``, the timing will increase

   |pic23| |pic24|

   |pic25|

   .. |pic23| image:: data/tuning/exp4/beta_alpha.png
      :width: 45%

   .. |pic24| image:: data/tuning/exp4/beta_beta.png
      :width: 45%

   .. |pic25| image:: data/tuning/exp4/beta_scale.png
      :width: 45%


- For ``lognormal`` (as below):

   - when we increase ``shape``, the timing will decrease
   - when we increase ``scale``, the timing will increase

   |pic26| |pic27|

   .. |pic26| image:: data/tuning/exp4/lognorm_shape.png
      :width: 45%

   .. |pic27| image:: data/tuning/exp4/lognorm_scale.png
      :width: 45%

- For ``exponweib`` (as below):

   - when we increase ``a``, the timing will decrease
   - when we increase ``c``, the timing will increase
   - when we increase ``scale``, the timing will increase

   |pic28| |pic29|

   |pic30|

   .. |pic28| image:: data/tuning/exp4/exponweib_a.png
      :width: 45%

   .. |pic29| image:: data/tuning/exp4/exponweib_c.png
      :width: 45%

   .. |pic30| image:: data/tuning/exp4/exponweib_scale.png
      :width: 45%

In order to tune the symptom trajectory, we can adjust the probability function in general, or target at a sepcfic trajectory.

.. code-block:: python

   symptom_trajectory:
   enable: true
   adjust_factor:
      general:
         beta:
         enable: true
         a: 1.0
         b: 1.0
         loc: 1.0
         scale: 0.3
         lognormal:
         enable: true
         s: 1.0
         loc: 1.0
         scale: 0.3
         exponweib:
         enable: true
         a: 1.0
         c: 1.0
         loc: 1.0
         scale: 0.3
      traj1:
         name: exposed => mild => severe => dead_home
         paras:
         - symptom_tag: exposed
            completion_time:
               type: beta
               a: 2.29
               b: 19.05
               loc: 0.39
               scale: 39.8



|pic19| |pic20|

|pic21| |pic22|

.. |pic19| image:: data/tuning/exp4/51150_infection_1.png
   :width: 45%

.. |pic20| image:: data/tuning/exp4/51150_infection_2.png
   :width: 45%

.. |pic21| image:: data/tuning/exp4/51440_infection_1.png
   :width: 45%

.. |pic22| image:: data/tuning/exp4/51440_infection_2.png
   :width: 45%


We can see that by reducing ``scale`` in the symptom trajectory, we can increase the symptom cycle easily.
