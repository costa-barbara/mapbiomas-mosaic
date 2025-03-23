#
import ee
from modules.BandNames import getBandNames
from pprint import pprint

ee.Initialize(project= "ee-barbaracostaipam")

def getMosaic(
        collection,
        percentileDry=25,
        percentileWet=75,
        percentileMin=5,  # New parameter for minimum mosaic
        percentileMax=95,  # New parameter for maximum mosaic
        percentileBand='ndvi',
        dateStart='2020-01-01',
        dateEnd='2021-01-01'):

    # Get band names and create suffixes
    bands = ee.Image(collection.first()).bandNames()

    bandsDry = bands.map(lambda band: ee.String(band).cat('_median_dry'))
    bandsWet = bands.map(lambda band: ee.String(band).cat('_median_wet'))
    bandsAmp = bands.map(lambda band: ee.String(band).cat('_amp'))

    # Calculate percentiles for dry and wet seasons
    dry = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileDry]))
    wet = collection.select([percentileBand]).reduce(ee.Reducer.percentile([percentileWet]))

    # Filter images for each season (dry and wet)
    collectionDry = collection.map(lambda image: image.mask(image.select([percentileBand]).lte(dry)))
    collectionWet = collection.map(lambda image: image.mask(image.select([percentileBand]).gte(wet)))

    # Reduce the collection to a median mosaic
    mosaic = collection.filter(ee.Filter.date(dateStart, dateEnd)).reduce(ee.Reducer.median())

    # Dry and wet season mosaics
    mosaicDry = collectionDry.reduce(ee.Reducer.median()).rename(bandsDry)
    mosaicWet = collectionWet.reduce(ee.Reducer.median()).rename(bandsWet)

    # Get percentiles mosaic
    mosaicMin = collection.reduce(ee.Reducer.percentile([percentileMin]))
    mosaicMax = collection.reduce(ee.Reducer.percentile([percentileMax]))

    # Calculating amplitude using percentiles
    mosaicAmp = mosaicMax.subtract(mosaicMin).rename(bandsAmp)

    # Standard deviation mosaic
    mosaicStdDev = collection.reduce(ee.Reducer.stdDev())

    # Add the bands to the final mosaic
    mosaic = mosaic\
        .addBands(mosaicDry)\
        .addBands(mosaicWet)\
        .addBands(mosaicMin.rename(bands.map(lambda band: ee.String(band).cat('_min')))))\
        .addBands(mosaicMax.rename(bands.map(lambda band: ee.String(band).cat('_max')))))\
        .addBands(mosaicAmp)\
        .addBands(mosaicStdDev)\
        .addBands(dry)\
        .addBands(wet)

    return mosaic
