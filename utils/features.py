from typing import Callable
import pandas as pd
import ee


WINDOW = 3 # Трехдневное окно в обе стороны

def onimage(image:ee.Image | ee.ImageCollection):
    def decorator(func):
        func.image = image
        func.raw_image = None
        return func
    return decorator

def enrich_features(fc: ee.FeatureCollection, images: list[tuple[str, Callable]]):
    def enrich(f: ee.Feature):
        point = f.geometry()
        date = ee.Date(f.get('date'))
        f_depth = ee.Number(f.get('fdepth'))
        
        start = date.advance(-WINDOW, 'day')
        end = date.advance(WINDOW, 'day')
        
        return f.set(
            {x: fun(
                point = point, 
                buffer = point.buffer(5000),
                start = start, 
                end = end, 
                depth = f_depth
                ) for x, fun in images}
        )
    return fc.map(enrich)

def update_dataframe(fc: ee.FeatureCollection, df: pd.DataFrame, properties: list[str]):
    results = fc.getInfo()['features']
    id_to_values = {
        f['properties']['id']: {x: f['properties'].get(x) for x in properties}
        for f in results
    }
    for property in properties:
        df[property] = [id_to_values.get(i, 0)[property] for i in df.index]