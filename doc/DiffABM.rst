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

The following figures show the outputs from different experiments:

.. tabularcolumns:: |p{5cm}|p{8cm}|p{5cm}|p{5cm}|

.. csv-table:: Experiment data
   :file: data/DeepABM_exp.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1 1

Experiment 1
===============

   |pic3| |pic4|

   .. |pic3| image:: data/prediction_vs_truth_exp1.png
      :width: 45%

   .. |pic4| image:: data/loss_exp1.png
      :width: 45%






