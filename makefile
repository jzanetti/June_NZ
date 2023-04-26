
override CONDA = $(CONDA_BASE)/bin/conda
override PIP = $(CONDA_BASE)/bin/pip3
override PKG=june_nz

create_env:
	$(CONDA) env create -n $(PKG) -f env.yml
	$(CONDA) activate $(PKG)
	$(PIP) install recordclass