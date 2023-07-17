##############
Combinining ABM and deep learning
##############

The tradional ABM is a prowerful tool that invovlves the social simulation of each individual in the model and addresses a series of "what-if"
questions, which can have long lasting implications on our future.

However, the real-world implementation of ABM can suffer from slow simulations due to the scale invovlved, and the model calibration becomes challenging and
very time-consuming due to the large number of parameters. To overcome these issues, `Ayush et al. (2023) <https://arxiv.org/pdf/2207.09714.pdf>`_
introduced a novel differentiable ABM framework called GradABM, which integrates the Gated Reccurrent Unit (GRU) with a tensorized ABM.). 

The GradABM framework offers significant advanatgaes over traditional ABM. 

There are significant advanatgaes for GradABM over a traditional ABM (see below):

   |pic1|

   .. |pic1| image:: data/abm_features.PNG
      :width: 100%

In June-NZ, we propose adopting the approach outlined in `Ayush et al. (2023) <https://arxiv.org/pdf/2207.09714.pdf>`_, and apply it in New Zealand's context.





