import ee
import math

#--------------------------------
# Terrain covariates
#--------------------------------
def getTerrainMetrics(image):
    """
    Added bands:
        - elevation: elevation above sea level, in meters.
        - slope: terrain slope, expressed as percent rise.
        - tpi: Topographic Position Index.
        - ruggedness: local standard deviation of elevation.
    """

    dem = ee.ImageCollection("projects/sat-io/open-datasets/FABDEM") \
        .mosaic() \
        .select('b1') \
        .rename('elevation') \
        .toFloat()

    slope_deg = ee.Terrain.slope(dem)

    slope_pct = slope_deg.expression(
        'tan(deg * pi / 180) * 100',
        {
            'deg': slope_deg,
            'pi': ee.Number(math.pi)
        }
    ).rename('slope').toFloat()

    # Kernel for local terrain metrics
    kernel = ee.Kernel.square(radius=3)

    mean_neighborhood = dem.reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel
    )

    tpi = dem.subtract(mean_neighborhood).rename('tpi').toFloat()

    ruggedness = dem.reduceNeighborhood(
        reducer=ee.Reducer.stdDev(),
        kernel=kernel
    ).rename('ruggedness').toFloat()

    return image \
        .addBands(slope_pct) \
        .addBands(tpi) \
        .addBands(ruggedness)
    
#--------------------------------
# Structural-context metrics
#--------------------------------
def getStructuralContext(image):
    """
    Adds reduced local structural-context metrics.

    Added bands:
        - gcvi_median_mean
        - gcvi_median_dry_mean
        - ndfi_median_dry_stdDev
     Notes:
        The kernel radius is 3 pixels, equivalent to a 7x7 local window
        at Landsat resolution.
    """

    kernel = ee.Kernel.square(radius=3)

    gcvi_mean = image.select('gcvi_median').reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel
    ).rename('gcvi_median_mean')

    gcvi_dry_mean = image.select('gcvi_median_dry').reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel
    ).rename('gcvi_median_dry_mean')

    ndfi_wet_std = image.select('ndfi_median_wet').reduceNeighborhood(
        reducer=ee.Reducer.stdDev(),
        kernel=kernel
    ).rename('ndfi_median_wet_stdDev')

    return image.addBands(gcvi_mean) \
        .addBands(gcvi_dry_mean) \
        .addBands(ndfi_wet_std)

#--------------------------------
# Textural for Rocky Outcrop Map
#--------------------------------
def getSpatialContext(image):
    """
    Adds lightweight spatial-context metrics for rocky outcrop mapping.

    Metrics:
        - local mean: neighborhood-level dominance of substrate/vegetation.
        - local stdDev: local heterogeneity / texture.
    """

    kernel = ee.Kernel.square(radius=3)  # 5x5 pixels 

    bands_context = [
        'bsi_median',
        'ndvi_median',
        'swir1_median'
    ]

    img_base = image.select(bands_context)

    reducer = ee.Reducer.mean().combine(
        reducer2=ee.Reducer.stdDev(),
        sharedInputs=True
    )

    context = img_base.reduceNeighborhood(
        reducer=reducer,
        kernel=kernel
    )

    return image.addBands(context)
