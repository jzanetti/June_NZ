from june.world import generate_world_from_geography
from june.geography.geography import Geography as Geography_class
from june.demography.demography import Demography as Demography_class

def create_world(geography: Geography_class, person: Demography_class):
    """Create the World class

    Args:
        geography (Geography_class): Geography class
        demography (Demography_class): Demography class

    Returns:
        _type_: _description_
    """
    return generate_world_from_geography(geography, demography=person)

