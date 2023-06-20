Toy model for JUNE_NZ
=====

A toy model can be used to test **JUNE_NZ**. 

The model data are stored at ``etc/data/singleobs_v2.0``, and the configuration file is ``etc/cfg/run/june_singleobs_v2.0.yml``.

The toy model contains 30 agents living in 2 super areas (``SA`` and ``SB``) and 3 areas (``A1``, ``A2`` and ``B1``). The characters of each agent are also made up and
can be customized according to different requirements.

The toy model can be run as:

.. code-block:: python

    python cli_june.py --workdir /tmp/june_singleobs_v2.0 --cfg etc/cfg/run/june_singleobs_v2.0.yml



