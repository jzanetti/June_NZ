##############
Combinining ABM and Neural Network
##############

The tradional ABM is a prowerful tool that invovlves the social simulation of each individual in the model and addresses a series of "what-if"
questions, which can have long lasting implications on our future.

However, the real-world implementation of ABM can suffer from slow simulations due to the scale invovlved, and the model calibration becomes challenging and
very time-consuming due to the large number of parameters. To overcome these issues, `Ayush et al. (2023) <https://arxiv.org/pdf/2207.09714.pdf>`_
introduced a novel differentiable ABM framework called GradABM, which integrates the Gated Reccurrent Unit (GRU) with a tensorized ABM.). 

The GradABM framework offers significant advanatgaes over traditional ABM:

   |pic1|

   .. |pic1| image:: data/abm_features.PNG
      :width: 100%

In June-NZ, we propose adopting the approach outlined in `Ayush et al. (2023) <https://arxiv.org/pdf/2207.09714.pdf>`_, and apply it in New Zealand's context.

Thw following equation summarizes the process of combinining a temporal based neural network (e.g., RNN, GRU or LSTM) with a tensorized ABM.


   |pic2|

   .. |pic2| image:: data/equation1.PNG
      :width: 70%

In contrast to the original paper, in JUNE_NZ:

- We have incorporated an additional uncertainty tensor in the neural network to account for agents that may not be adequately represented by the input graph representations.
- Instead of using GRU, an LSTM is used to generate the condensed representations of temporal evolution of disease characteristics
- The number of learnable parmaters are increased from 3 to 8 (covering the parameters from ``mortality rate``, ``exposed to infected time`` to a bunch of infection related  __Gamma__ function paramters.).


**********
Results comparisons
**********

The following figures show the outputs from various experiments. 
The model (if a neural network is applied) is trained using a sample dataset from New Zealand,
which has a population of 100,000, and the death rate of COVID-19 in May and June 2021.

.. tabularcolumns:: |p{5cm}|p{8cm}|p{5cm}|p{5cm}|

.. csv-table:: Experiment configuration (70 days simulation)
   :file: data/DeepABM_exp.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1 1

The edges for the graph network for different types of interaction groups can be seen below (the x-axis represents different ``venues``, while the y-axis shows the number of people in that particular ``venue``):

   |pic12| |pic13|
   |pic14| |pic15|
   |pic16| |pic17|
   |pic18| |pic19|
   |pic20|

   .. |pic12| image:: data/gradabm/interaction_diags_cinema.png
      :width: 45%

   .. |pic13| image:: data/gradabm/interaction_diags_grocery.png
      :width: 45%

   .. |pic14| image:: data/gradabm/interaction_diags_gym.png
      :width: 45%

   .. |pic15| image:: data/gradabm/interaction_diags_pub.png
      :width: 45%

   .. |pic16| image:: data/gradabm/interaction_diags_city_transport.png
      :width: 45%

   .. |pic17| image:: data/gradabm/interaction_diags_inter_city_transport.png
      :width: 45%

   .. |pic18| image:: data/gradabm/interaction_diags_company.png
      :width: 45%

   .. |pic19| image:: data/gradabm/interaction_diags_school.png
      :width: 45%

   .. |pic20| image:: data/gradabm/interaction_diags_household.png
      :width: 45%

Experiment 1
===============

   |pic3| |pic4|
   |pic5|

   .. |pic3| image:: data/prediction_vs_truth_exp1.png
      :width: 45%

   .. |pic4| image:: data/loss_exp1.png
      :width: 45%

   .. |pic5| image:: data/agents_exp1.png
      :width: 45%


Experiment 2
===============

   |pic6| |pic7|
   |pic8|

   .. |pic6| image:: data/prediction_vs_truth_exp2.png
      :width: 45%

   .. |pic7| image:: data/loss_exp2.png
      :width: 45%

   .. |pic8| image:: data/agents_exp2.png
      :width: 45%

Experiment 3
===============

   |pic9| |pic10|
   |pic11|

   .. |pic9| image:: data/prediction_vs_truth_exp3.png
      :width: 45%

   .. |pic10| image:: data/loss_exp3.png
      :width: 45%

   .. |pic11| image:: data/agents_exp3.png
      :width: 45%





