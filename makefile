
override CONDA = $(CONDA_BASE)/bin/conda
override PKG=june_nz

clear_env:
	rm -rf $(CONDA_BASE)/envs/$(PKG)

clear_all:
	rm -rf $(CONDA_BASE)/envs/$(PKG)
	rm -rf $(CONDA_BASE)/pkgs/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/.cache/paths/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/linux-64/.cache/recipe/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/.cache/paths/$(PKG)*
	rm -rf $(CONDA_BASE)/conda-bld/osx-arm64/.cache/recipe/$(PKG)*
	# $(CONDA) index $(CONDA_BASE)/conda-bld

create_env: clear_all clear_env
	$(CONDA) env create -n $(PKG) -f env.yml
	$(CONDA_BASE)/envs/$(PKG)/bin/pip3 install recordclass