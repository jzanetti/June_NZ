Installation
=====

This page contains the instructions about how to install **JUNE_NZ**

The package management tool ``mamba`` is required for installing **JUNE_NZ**. Please install it before the instruction or contact your Linux administor

MAMBA Installation
^^^^^^^^^
**MAMBA** is a package manager which support multiple languages including python. It can be installed as below:

- **Step 1**: download `miniconda` from  `[here] <https://docs.conda.io/en/latest/miniconda.html>`_
- **Step 2**: the package can be installed as ``bash Miniconda3-latest-Linux-x86_64.sh``, or following the instruction `[here] <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html>`_
- **Step 3**: install mamba by ``conda install mamba -c conda-forge``


JUNE_NZ environment
^^^^^^^^^
After ``mamba``, **JUNE_NZ** can be simply installed with the provided ``makefile`` in the repository:

.. code-block:: bash

   export CONDA_BASE=<CONDA PATH>
   make create_env

where ``CONDA_BASE`` is the path where the ``conda`` package is installed. For example, we can have ``export CONDA_BASE=~/Programs/miniconda3/``.

The ``make`` command creates a conda environment ``june_nz``, which contains all the dependancies for running **JUNE_NZ**.

The working environment then can be activated as:

.. code-block:: bash

   conda activate june_nz

