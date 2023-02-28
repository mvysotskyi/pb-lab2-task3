"""
Module used to create the map.
"""

from folium import Map, Marker, Popup, Icon

def read_countries_dataset(filepath: str) -> dict[str, tuple[float, float]]:
    """
    Function reads dataset with countries codes and locations.
    """
    countries = {}
    with open(filepath, 'r', encoding="utf-8") as file:
        file.readline()
        for line in file.readlines():
            line = [part.strip('"') for part in line.strip().split(',')]
            countries[line[0]] = (float(line[-2]), float(line[-1]))

    return countries

def create_map(points: list[tuple[float, float, str]]) -> Map:
    """
    Function creates map with markers.
    """
    world_map = Map(
        location=[0, 0],
        zoom_start=4,
        min_zoom=2,
        tiles='stamentoner',
        max_bounds=True
    )

    for point in points:
        marker = Marker(
            location=[point[0], point[1]],
            popup=Popup(point[2]),
            icon=Icon(color="green", icon='music')
        )
        marker.add_to(world_map)

    return world_map
