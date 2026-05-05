import ee
import pandas as pd
REGION_PADDING = 2

def calc_region(lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> ee.Geometry:
    lat_min = max(0, lat_min-REGION_PADDING)
    lon_min = max(0, lon_min-REGION_PADDING)
    lat_max = min(360, lat_max+REGION_PADDING)
    lon_max = min(360, lon_max+REGION_PADDING)
    return ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max], geodesic=False)
    
def region_from_df(lat: pd.Series, lon: pd.Series) -> ee.Geometry:
    lat_mod = lat
    lon_mod = (lon+360).mod(360)
    return calc_region(lat_mod.min(), lat_mod.max(), lon_mod.min(), lon_mod.max())