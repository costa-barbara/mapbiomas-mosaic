#
import ee
from pprint import pprint

# Initialize Earth Engine with specific project (adjust to your environment)
ee.Initialize(project= "ee-barbaracostaipam")

# Builds a comprehensive mosaic from a monthly Landsat ImageCollection, 
# including seasonal medians, amplitude, percentiles, and standard deviation.
def getMosaic(
        collection,
        percentileDry=25,
        percentileWet=75,
        percentileMin=5,  # New parameter for minimum mosaic
        percentileMax=65,  # New parameter for maximum mosaic
        percentileBand='ndvi',
        dateStart='2020-01-01',
        dateEnd='2021-01-01'):

    """
    Constructs a multi-layered mosaic from a monthly Landsat ImageCollection.

    Parameters:
        collection (ee.ImageCollection): Monthly Landsat mosaic collection.
        percentileDry (int): NDVI percentile for dry season threshold (default: 25).
        percentileWet (int): NDVI percentile for wet season threshold (default: 75).
        percentileMin (int): Lower percentile for amplitude computation (default: 5).
        percentileMax (int): Upper percentile for amplitude computation (default: 65).
        percentileBand (str): Band used to define dry/wet conditions (default: 'ndvi').
        dateStart (str): Start date for temporal filtering (inclusive).
        dateEnd (str): End date for temporal filtering (exclusive).

    Returns:
        ee.Image: Final mosaic containing seasonal medians, percentiles, 
                  amplitude, median standard deviation, and dry/wet NDVI thresholds.
    """

    # Get original band names
    bands = ee.Image(collection.first()).bandNames()

    # Generate suffixes for renamed output bands
    bandsDry = bands.map(lambda band: ee.String(band).cat('_median_dry'))
    bandsWet = bands.map(lambda band: ee.String(band).cat('_median_wet'))
    
    # Compute NDVI percentiles to define dry and wet seasons
    dry = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileDry]))
    wet = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileWet]))

    # Mask collections by dry and wet season thresholds
    collectionDry = collection.map(lambda image: image.mask(image.select([percentileBand]).lte(dry)))
    collectionWet = collection.map(lambda image: image.mask(image.select([percentileBand]).gte(wet)))

    # Filter full collection to the date range and compute the median mosaic
    mosaic = collection.filter(ee.Filter.date(dateStart, dateEnd)).reduce(ee.Reducer.median())

    # Generate seasonal mosaics using the masked collections
    mosaicDry = collectionDry.reduce(ee.Reducer.median()).rename(bandsDry)
    mosaicWet = collectionWet.reduce(ee.Reducer.median()).rename(bandsWet)

    # Compute percentile mosaics for amplitude
    mosaicMin = collection.reduce(ee.Reducer.percentile([percentileMin]))
    mosaicMax = collection.reduce(ee.Reducer.percentile([percentileMax]))

    # Compute Median Absolute Deviation (MAD) across time series
    mosaicMedian = collection.reduce(ee.Reducer.median())
    mosaicStdDev = collection.map(lambda img: img.subtract(mosaicMedian).abs())\
                  .reduce(ee.Reducer.median())\
                  .rename(bands.map(lambda b: ee.String(b).cat('_stdDev')))
    
    # Compute  Coefficient of Variation (MAD / median)
    mosaicCVR = mosaicStdDev.divide(mosaicMedian).rename(bands.map(lambda b: ee.String(b).cat('_cvr')))

    # Rename min and max bands
    mosaicMin = mosaicMin.rename(bands.map(lambda band: ee.String(band).cat('_min')))
    mosaicMax = mosaicMax.rename(bands.map(lambda band: ee.String(band).cat('_max')))   

    # Combine all components into final mosaic
    mosaic = mosaic\
        .addBands(mosaicDry)\
        .addBands(mosaicWet)\
        .addBands(mosaicMin)\
        .addBands(mosaicMax)\
        .addBands(mosaicStdDev)\
        .addBands(mosaicCVR)\
        .addBands(dry)\
        .addBands(wet)

    return mosaic
