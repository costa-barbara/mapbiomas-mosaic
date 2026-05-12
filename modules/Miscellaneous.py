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

def getSlope(image):
    """
    Adds a slope band (percent) to the input image, derived from the MERIT DEM.
    """
    
    # Load MERIT DEM and compute slope in degrees
    terrain = ee.Image("MERIT/DEM/v1_0_3").select('dem')
    slope_deg = ee.Terrain.slope(terrain)
    
    # Convert slope from degrees to percent: tan(deg * pi / 180) * 100
    slope_pct = slope_deg.expression(
      'tan (pi/180 * deg) * 100', {
        'deg': slope_deg,
        'pi': ee.Number(math.pi)
      }).rename('slope').toInt16()

    return image.addBands(slope_pct)
    
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
        - tcb_median_stdDev
    """

    kernel = ee.Kernel.square(radius=3)

    gcvi_mean = image.select('gcvi_median').reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel,
        optimization='boxcar'
    ).rename('gcvi_median_mean')

    gcvi_dry_mean = image.select('gcvi_median_dry').reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel,
        optimization='boxcar'
    ).rename('gcvi_median_dry_mean')

    ndfi_dry_std = image.select('ndfi_median_dry').reduceNeighborhood(
        reducer=ee.Reducer.stdDev(),
        kernel=kernel
    ).rename('ndfi_median_dry_stdDev')

    tcb_std = image.select('tcb_median').reduceNeighborhood(
        reducer=ee.Reducer.stdDev(),
        kernel=kernel
    ).rename('tcb_median_stdDev')

    return image \
        .addBands(gcvi_mean) \
        .addBands(gcvi_dry_mean) \
        .addBands(ndfi_dry_std) \
        .addBands(tcb_std)

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
