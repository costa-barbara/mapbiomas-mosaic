#
import ee
from modules.BandNames import getBandNames
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
        percentileMax=95,  # New parameter for maximum mosaic
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
        percentileMax (int): Upper percentile for amplitude computation (default: 95).
        percentileBand (str): Band used to define dry/wet conditions (default: 'ndvi').
        dateStart (str): Start date for temporal filtering (inclusive).
        dateEnd (str): End date for temporal filtering (exclusive).

    Returns:
        ee.Image: Final mosaic containing seasonal medians, percentiles, 
                  amplitude, median absolute deviation, and dry/wet NDVI thresholds.
    """

    # Get original band names
    bands = ee.Image(collection.first()).bandNames()

    # Generate suffixes for renamed output bands
    bandsDry = bands.map(lambda band: ee.String(band).cat('_median_dry'))
    bandsWet = bands.map(lambda band: ee.String(band).cat('_median_wet'))

    bandsMin = bands.map(lambda band: ee.String(band).cat('_min'))
    bandsMax = bands.map(lambda band: ee.String(band).cat('_max'))
    bandsAmp = bands.map(lambda band: ee.String(band).cat('_amp'))

    bandsP25 = bands.map(lambda band: ee.String(band).cat('_p25'))
    bandsP75 = bands.map(lambda band: ee.String(band).cat('_p75'))
    bandsIQR = bands.map(lambda band: ee.String(band).cat('_iqr'))

    bandsMad = bands.map(lambda band: ee.String(band).cat('_mad'))

    # Compute NDVI percentiles to define dry and wet seasons
    dry = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileDry]))
    wet = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileWet]))

    # Mask collections by dry and wet season thresholds
    collectionDry = collection.map(lambda image: image.mask(image.select([percentileBand]).lte(dry)))
    collectionWet = collection.map(lambda image: image.mask(image.select([percentileBand]).gte(wet)))

    # Filter entire collection to the date range and compute the median mosaic
    mosaic = collection.filter(ee.Filter.date(dateStart, dateEnd)).reduce(ee.Reducer.median())

    # Generate seasonal mosaics using the masked collections
    mosaicDry = collectionDry.reduce(ee.Reducer.median()).rename(bandsDry)
    mosaicWet = collectionWet.reduce(ee.Reducer.median()).rename(bandsWet)

    # Compute percentile mosaics for amplitude
    mosaicMin = collection.reduce(ee.Reducer.percentile([percentileMin])).rename(bandsMin)
    mosaicMax = collection.reduce(ee.Reducer.percentile([percentileMax])).rename(bandsMax)

    # Compute amplitude (max - min)
    mosaicAmp = mosaicMax.subtract(mosaicMin).rename(bandsAmp)

    # Interquartile range: p75 - p25
    mosaicP25 = collection.reduce(ee.Reducer.percentile([25])).rename(bandsP25)
    mosaicP75 = collection.reduce(ee.Reducer.percentile([75])).rename(bandsP75)
    mosaicIQR = mosaicP75.subtract(mosaicP25).rename(bandsIQR)

    # Median absolute deviation from temporal median
    median = collection.reduce(ee.Reducer.median()).rename(bands)

    absDeviationCollection = collection.map(lambda image: image.subtract(median).abs())

    mosaicMad = absDeviationCollection.reduce(ee.Reducer.median()).rename(bandsMad)

    # Combine all components into final mosaic
    mosaic = mosaic\
        .addBands(mosaicDry)\
        .addBands(mosaicWet)\
        .addBands(mosaicMin)\
        .addBands(mosaicMax)\
        .addBands(mosaicAmp)\
        .addBands(mosaicIQR)\
        .addBands(mosaicMad)\
        .addBands(dry)\
        .addBands(wet)

    return mosaic
