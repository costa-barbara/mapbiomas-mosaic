import ee
import math

# Terrain covariates
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

# Structural-context metrics
def getStructuralContext(image):
    """
    Adds local structural-context metrics derived from spectral index bands.

    This function computes neighborhood-level mean and standard deviation for
    selected spectral indices. These metrics are intended to capture local
    vegetation structure and spatial heterogeneity, supporting the separation
    of spectrally similar Cerrado classes such as savanna, grassland, and
    pasture.

    Parameters:
        image (ee.Image): Image containing 'index_median'.

    Returns:
        ee.Image: Input image with additional structural context bands:
            - index_median_mean
            - index_median_stdDev

    """

    # Define a local neighborhood window.
    # This window size is intended to capture local structural context while reducing excessive smoothing across class boundaries.
    kernel = ee.Kernel.square(radius=3)

    # Spectral index bands selected for local structural analysis.
    structural_bands = [
        'gcvi_median',
        'gcvi_median_dry',
        'ndfi_median_dry',
    ]

    image_base = image.select(structural_bands)

    # Combined reducer to compute local mean and local standard deviation
    # in a single neighborhood operation.
    reducer = ee.Reducer.mean().combine(
        reducer2=ee.Reducer.stdDev(),
        sharedInputs=True
    )

    structural_context = image_base.reduceNeighborhood(
        reducer=reducer,
        kernel=kernel
    )

    return image.addBands(structural_context)

# Textural for Rocky Outcrop Map
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
