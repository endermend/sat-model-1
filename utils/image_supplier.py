import geemap
import ee

def supply(layer_function: callable[[geemap.Map], None], m: geemap.Map, ebsRegion: ee.Geometry = None, filter: ee.Filter = None):
    if layer_function.raw_image is None:
        layer_function.raw_image = layer_function.image
    layer_function.image = layer_function.raw_image
    if filter is not None:
        layer_function.image = layer_function.image.filter(filter)
    if isinstance(layer_function.image, ee.ImageCollection):
        layer_function.image = layer_function.image.mean()
    if ebsRegion is not None:
        layer_function.image = layer_function.image.clip(ebsRegion)
    layer_function(m)