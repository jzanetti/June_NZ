
# JUNE model for New Zealand

### Installation
The package can be installed using:

```
export CONDA_BASE=~/miniconda3
make create_env
```


### Required data:

#### Disease:
- `covid19.yaml`: infection transmission profile defination (geography independant)
- `symptom_trajectories.yaml`: symptom trajectories profile defination (geography independant)
- `infection_outcome_ratio.csv`: infection outcome for people with different ages (geography independant)

#### Group:
- `household`:
  - `household_structure.yaml`: basic household configuration (geography independant)
  - `age_difference_couple.csv`: couple age difference (geography independant)
  - `age_difference_parent_child.csv`: parent-child age difference (geography independant)
  - `household_commual.csv`: communal house number (area level)
  - `household_student.csv`: student house number (area level)
  - `household_number.csv`: regular house number (area level)

- `company`:
  - `company_closure.yaml`: company closure policy when lockdown (geography independant)
  - `employees_by_super_area.csv`:  company numbers for different ages  (super area level)
  - `sectors_by_super_area.csv`: company numbers for differetn sectors (super area level)
  - `sectors_employee_genders.csv`: company employees for different genders (area level)
  - `subsector_cfg.yaml`: Sub sector defination (geography independant)

- `hospital`:
  - `hospital_config.yaml`: basic hospital configuration (geography independant)
  - `neighbour_hospitals.yaml`: nearby hospital (geography independant)
  - `hospital_locations.csv`: hospital locations (area level)

- `commute`:
  - `mode_of_transport.yaml`: the category (public or private) for each transport method (geography independant)
  - `passage_seats_ratio.yaml`: Seats per passenger (region level)
  - `stations.yaml`: number of inter city stations (super area level)
  - `super_area_name.csv`: super area names (super area level)
  - `transport_mode.csv`: number of people travelling with different transport method (Area level)

- `others`:
  - `workplace_and_home.csv`: the places where people live and work (super area level) 

#### interaction:
- `general.yaml`: general interaction configuration (geography independant)
- `<group>.yaml`: group contact matrix (geography independant)

#### policy:
- `policy.yaml`: Policy setups (e.g., lockdown etc.) (geography independant)

#### demography:
- `age_profile.csv`: people number ~ age profile (area level)
- `ethnicity_profile.csv`: ethnicity ~ age profile (area level)
- `gender_profile_female_ratio.csv`: gender ratio ~ age profile (area level)
- `comorbidities_<csv>.csv`: comorbidities ~ age profile (geography independant)

#### geography:
- `area_location.csv`: area location (area level)
- `super_area_location.csv`: super area location (super area level)
- `area_socialeconomic_index.csv`: social economic index (area level)
- `geography_hierarchy_definition.csv`: geography hierarchy (geography independant)