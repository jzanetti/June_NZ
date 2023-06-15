from time import sleep

import overpy
from geopy.geocoders import Nominatim

api = overpy.Overpass()

from logging import getLogger

from process import OVERPY_QUERY_KEY

logger = getLogger()


def get_data_from_osm(
    name: str,
    super_area_id: str,
    geo_name: str,
    output: dict,
    radius: int = 500.0,
    domain_range: dict = {"lat": [-50.0, -30.0], "lon": [160.0, 180.0]},
) -> list:
    """Query data from OSM

    Args:
        name (str): the amenity type, e.g., cinema
        geo_name (str): city or region name, e.g., Wellington
        radius (float, default: 500): Query radius in km

    Returns:
        list: the queried results from OSM
    """
    geolocator = Nominatim(user_agent="{name}_extraction")
    location = geolocator.geocode(f"{geo_name}, New Zealand")
    lat = location.latitude
    lon = location.longitude

    radius *= 1000.0

    proc_query_key = OVERPY_QUERY_KEY[name]

    query = "("
    for query_key in proc_query_key:
        proc_data_list = proc_query_key[query_key]

        for proc_data_name in proc_data_list:
            query += f'node["{query_key}"="{proc_data_name}"](around:{radius},{lat},{lon});'

    query = query + "); \nout;"

    tried = 0
    while True:
        try:
            result = api.query(query)
            break
        except:
            if tried > 3:
                raise Exception("Tried too many times, give up ...")
            logger.info(
                f"Too many requests or timeout for {name} in {geo_name}, waiting 10 seconds to try again ..."
            )
            sleep(10)
            tried += 1

    if len(result.nodes) == 0:
        logger.info(f"Not able to find {name} in {geo_name} ...., please be careful about thie !")

    for node in result.nodes:
        node_lat = float(node.lat)
        node_lon = float(node.lon)

        if (
            node_lat > domain_range["lat"][1]
            or node_lat < domain_range["lat"][0]
            or node_lon < domain_range["lon"][0]
            or node_lat > domain_range["lon"][1]
        ):
            raise Exception(f"Seems there is an issue for locating {name} in {geo_name}")

        output["lat"].append(float(node.lat))
        output["lon"].append(float(node.lon))
        output["super_area"].append(super_area_id)

        """
        proc_output = {
            "name": node.tags.get("name", ""),
            "lat": node.lat,
            "lon": node.lon,
            "address": node.tags.get("addr:full", ""),
            "capacity": node.tags.get("capacity", "Unknown"),
        }
        output.append(proc_output)
        """

    return output
