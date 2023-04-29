from june.world import generate_world_from_geography
from june.geography.geography import Geography as Geography_class
from june.demography.demography import Demography as Demography_class
from copy import deepcopy
from pandas import DataFrame
from datetime import datetime
from june.world import World as World_class
from os.path import join


def create_world(geography: Geography_class, person: Demography_class) -> World_class:
    """Create the World class

    Args:
        geography (Geography_class): Geography class
        demography (Demography_class): Demography class

    Returns:
        World_class: _description_
    """
    return generate_world_from_geography(geography, demography=person)


def world2df(world_input: World_class, time: datetime = None, write_csv: bool = False, workdir: str = None, tag: str = ""):
    """Convert the world object to a dataframe

    Args:
        world_input (World_class): An world object
        time (datetime, optional): Time to write. Defaults to None.
        write_csv (bool, optional): Read CSV file
        workdir (str, optional): Working directory

    Returns:
        dict: The dict contains the dataframe
    """
    my_world = deepcopy(world_input)
    all_areas = my_world.areas

    household_info = {
        "super_area_name": [],
        "area_name": [],
        "area_population": [],
        "area_socialeconomic_index": [],
        "composition_type": [],
        "being_visited": [],
        "contains_people": [],
        "coordinates": [],
        "n_residents": [],
        "size": [],
        "type": []

    }

    person_info = {
        "id": [],
        "time": [],
        "super_area_name": [],
        "area_name": [],
        "household_id": [],
        "sex": [],
        "age": [],
        "ethnicity": [],
        "work_sector": [],
        "sub_sector": [],
        "lockdown_status": [],
        "comorbidity": [],
        "busy": [],
        "work_super_area": [],
        "residence_super_area": [],
        "num_housemates": [],
        "work_city": [],
        "home_city": [],
        "transport_method": [],
        "transport_public": [],
        "commute": [],
        "residence_group_type": [],
        "residence_subgroup_type": [],
        "residence_external": [],
        "infected": [],
        "infection": [],
        "intensive_care": [],
        "symptoms": []

    }

    cities_info = {
        "work_city_name": [],
        "coordinates": [],
        "num_city_stations": [],
        "num_inter_city_stations": [],
        "travel_within_the_city": [],
        "travel_to_this_city_from_others": []
    }

    all_citieis = world_input.cities
    if all_citieis is not None:
        for proc_city in all_citieis.members:
            cities_info["work_city_name"].append(proc_city.name)
            cities_info["coordinates"].append(proc_city.coordinates)
            cities_info["num_city_stations"].append(len(proc_city.city_stations.members))
            cities_info["num_inter_city_stations"].append(len(proc_city.inter_city_stations.members))
            cities_info["travel_within_the_city"].append(proc_city.internal_commuter_ids)
            cities_info["travel_to_this_city_from_others"].append(proc_city.super_area.closest_inter_city_station_for_city[proc_city.name].commuter_ids)


    for proc_area in all_areas.members:
        
        super_area_name = proc_area.super_area.name
        area_name = proc_area.name
        area_population = len(proc_area.people)
        area_socialeconomic_index = proc_area.socioeconomic_index

        # Print household
        for proc_household in proc_area.households:

            household_info["super_area_name"].append(super_area_name)
            household_info["area_name"].append(area_name)
            household_info["area_population"].append(area_population)
            household_info["area_socialeconomic_index"].append(area_socialeconomic_index)
            household_info["composition_type"].append(proc_household.composition_type)
            household_info["being_visited"].append(proc_household.being_visited)
            household_info["contains_people"].append(proc_household.contains_people)
            household_info["coordinates"].append(proc_household.coordinates)
            household_info["n_residents"].append(proc_household.n_residents)
            household_info["size"].append(proc_household.size)
            household_info["type"].append(proc_household.type)

            for proc_person in proc_household.people:

                if time is not None:
                    person_info["time"].append(time)
                else:
                    person_info["time"].append(None)

                person_info["id"].append(proc_person.id)
                person_info["super_area_name"].append(super_area_name)
                person_info["area_name"].append(area_name)
                person_info["household_id"].append(proc_household.id)
                person_info["sex"].append(proc_person.sex)
                person_info["age"].append(proc_person.age)
                person_info["ethnicity"].append(proc_person.ethnicity)
                person_info["work_sector"].append(proc_person.sector)
                person_info["sub_sector"].append(proc_person.sub_sector)
                person_info["lockdown_status"].append(proc_person.lockdown_status)
                person_info["comorbidity"].append(proc_person.comorbidity)
                person_info["busy"].append(proc_person.busy)
                person_info["residence_group_type"].append(proc_person.residence.group.type)
                person_info["residence_subgroup_type"].append(proc_person.residence.group.subgroup_type)
                person_info["residence_external"].append(proc_person.residence.external)
                person_info["infected"].append(proc_person.infected)

                if proc_person.infection is not None:
                    person_info["infection"].append(proc_person.infection)
                else:
                    person_info["infection"].append(None)

                person_info["intensive_care"].append(proc_person.intensive_care)

                if proc_person.symptoms is not None:
                    person_info["symptoms"].append(proc_person.symptoms)
                else:
                    person_info["symptoms"].append(None)

                if proc_person.work_super_area is not None:
                    person_info["work_super_area"].append(proc_person.work_super_area.name)
                else:
                    person_info["work_super_area"].append(None)
                person_info["residence_super_area"].append(proc_person.super_area.name)
                person_info["num_housemates"].append(len(proc_person.housemates))

                if proc_person.work_city is not None:
                    person_info["work_city"].append(proc_person.work_city.name)
                else:
                    person_info["work_city"].append(None)


                if proc_person.home_city is not None:
                    person_info["home_city"].append(proc_person.home_city.name)
                else:
                    person_info["home_city"].append(None)

                if proc_person.mode_of_transport is not None:
                    person_info["transport_method"].append(proc_person.mode_of_transport.description)
                    person_info["transport_public"].append(proc_person.mode_of_transport.is_public)
                else:
                    person_info["transport_method"].append(None)
                    person_info["transport_public"].append(None)

                person_info["commute"].append(proc_person.commute)

    output = {
        "household": DataFrame.from_dict(household_info),
        "person": DataFrame.from_dict(person_info),
        "city": DataFrame.from_dict(cities_info)
    }

    if write_csv:
        for output_key in output:
            output[output_key].to_csv(join(workdir, f"{output_key}_{tag}.csv"))

    return output
