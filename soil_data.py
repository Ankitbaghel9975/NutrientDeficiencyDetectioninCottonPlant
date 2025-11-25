import geopandas as gpd

soil_gdf = gpd.read_file("Nagpur_dist.shp")

def get_soil_condition(lat: float, lon: float):
    """
    Given lat/lon → returns soil condition from shapefile.
    """
    point = gpd.points_from_xy([lon], [lat], crs=soil_gdf.crs)
    match = soil_gdf[soil_gdf.contains(point[0])]
    if not match.empty:
        return match.iloc[0].to_dict()
    return {"soil_type": "Unknown", "ph": "NA", "fertility": "NA"}
