import ee
import math

# Terrain covariates
def getTerrain(image):
    """
    Added bands:
        - elevation: elevation above sea level, in meters.
        - slope: terrain slope, expressed as percent rise.
        - tpi: Topographic Position Index, calculated as the difference between
          the pixel elevation and the mean elevation of its local neighborhood.

    Parameters:
        image (ee.Image):
            Input image to which the terrain covariates will be added.

    Returns:
        ee.Image:
            Input image with the additional terrain bands:
            ['elevation', 'slope', 'tpi'].
    """

    # Load and mosaic FABDEM
    # The original FABDEM collection is distributed as image tiles.
    dem = ee.ImageCollection("projects/sat-io/open-datasets/FABDEM") \
        .mosaic() \
        .select('b1') \
        .rename('elevation') \
        .toFloat()

    # Compute terrain slope in degrees from the elevation model.
    slope_deg = ee.Terrain.slope(dem)

    # Convert slope from degrees to percent rise:
    # slope (%) = tan(slope degrees * pi / 180) * 100
    slope_pct = slope_deg.expression(
        'tan(deg * pi / 180) * 100',
        {
            'deg': slope_deg,
            'pi': ee.Number(math.pi)
        }
    ).rename('slope').toFloat()

    # Compute Topographic Position Index (TPI).
    # TPI = elevation of the focal pixel - mean elevation of the neighborhood.
    # Positive values indicate locally higher positions; negative values
    # indicate locally lower positions.
    kernel = ee.Kernel.square(radius=5)  # ~330 m

    mean_neighborhood = dem.reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel
    )

    tpi = dem.subtract(mean_neighborhood).rename('tpi').toFloat()

    return image.addBands(dem).addBands(slope_pct).addBands(tpi)

# Terrain metrics for Rocky Outcrop Map
def getTerrainMetrics(image):
    """
    Added bands:
        - elevation: elevation above sea level, in meters.
        - slope: terrain slope, expressed as percent rise.
        - tpi: Topographic Position Index.
        - ruggedness: local standard deviation of elevation.
        - tri: Terrain Ruggedness Index, based on local absolute elevation differences.
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
    kernel = ee.Kernel.square(radius=5)  # ~330 m

    mean_neighborhood = dem.reduceNeighborhood(
        reducer=ee.Reducer.mean(),
        kernel=kernel
    )

    tpi = dem.subtract(mean_neighborhood).rename('tpi').toFloat()

    ruggedness = dem.reduceNeighborhood(
        reducer=ee.Reducer.stdDev(),
        kernel=kernel
    ).rename('ruggedness').toFloat()

    tri = dem.subtract(mean_neighborhood) \
        .abs() \
        .rename('tri') \
        .toFloat()

    return image \
        .addBands(slope_pct) \
        .addBands(tpi) \
        .addBands(ruggedness) \
        .addBands(tri)

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
    #
    # Kernel radius = 4 pixels.
    # At 30 m spatial resolution, this corresponds to a 9 x 9 pixel window,
    # or approximately 270 x 270 m.
    #
    # This window size is intended to capture local structural context while
    # reducing excessive smoothing across class boundaries.
    kernel = ee.Kernel.square(radius=4)

    # Spectral index bands selected for local structural analysis.
    structural_bands = [
        'gcvi_median',
        'gcvi_median_dry',
        'ndfi_median',
        'ndfi_median_dry'
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
def getGLCMTexture(image, band='swir1'):
    """
    Adds selected GLCM texture metrics from a mineral-sensitive band.

    The input band is rescaled to byte because ee.Image.glcmTexture()
    requires integer input. 
    """

    texture_input = image.select(band) \
        .unitScale(0, 10000) \
        .multiply(255) \
        .toByte()

    glcm = texture_input.glcmTexture(size=3)

    selected = glcm.select([
        f'{band}_contrast',
        f'{band}_var',
        f'{band}_idm',
        f'{band}_asm',
        f'{band}_corr'
    ])

    return image.addBands(selected)
