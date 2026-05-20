#!/usr/bin/env python

import ee, math

def rescale(image, min=0, max=10000):

    image = ee.Image(image)

    image = image.subtract(min) \
        .divide(ee.Number(max).subtract(min))

    return image

def cloudScoreMask(image, cloudThresh):

    image = ee.Image(image)
    
    score = ee.Image(1.0)

    # Clouds are reasonably bright in the blue band.
    blue = image.select(['blue'])
    score = score.min(rescale(blue, min=1000, max=3000))

    # Clouds are reasonably bright in all visible bands.
    visibleSum = image.expression("b('red') + b('green') + b('blue')")
    score = score.min(rescale(visibleSum, min=2000, max=8000))

    # Clouds are reasonably bright in all infrared bands.
    infraredSum = image.expression("b('nir') + b('swir1') + b('swir2')")
    score = score.min(rescale(infraredSum, min=3000, max=8000))

    # temperature = image.select('temp') # Sentinel 2 images doesn't have thermal band

    # However, clouds are not snow.
    ndsi = image.normalizedDifference(['green', 'swir1'])
    # score = score.min(rescale(ndsi, min=8000, max=6000))
    score = score.min(rescale(ndsi, min=0.8, max=0.6))

    # reescale score
    score = score.multiply(100).byte()
    score = score.gte(cloudThresh).rename('cloudScoreMask')

    return image.addBands(score)

def tdom(collection,
         zScoreThresh=-1,
         shadowSumThresh=5000,
         dilatePixels=2):

    shadowSumBands = ['nir', 'swir1']

    irStdDev = collection \
        .select(shadowSumBands) \
        .reduce(ee.Reducer.stdDev())

    irMean = collection \
        .select(shadowSumBands) \
        .mean()

    def _maskDarkOutliers(image):
        zScore = image.select(shadowSumBands) \
            .subtract(irMean) \
            .divide(irStdDev)

        irSum = image.select(shadowSumBands) \
            .reduce(ee.Reducer.sum())

        tdomMask = zScore.lt(zScoreThresh) \
            .reduce(ee.Reducer.sum()) \
            .eq(2) \
            .And(irSum.lt(shadowSumThresh)) \

        tdomMask = tdomMask.focal_min(dilatePixels)

        return image.addBands(tdomMask.rename('tdomMask'))

    collection = collection.map(_maskDarkOutliers)

    return collection

def cloudProject(image,
                 cloudBand=None,
                 shadowSumThresh=5000,
                 cloudHeights=[],
                 dilatePixels=2):

    cloud = image.select([cloudBand])

    # Get TDOM mask
    tdomMask = image.select(['tdomMask'])

    darkPixels = image.select(['nir', 'swir1', 'swir2']) \
        .reduce(ee.Reducer.sum()) \
        .lt(shadowSumThresh)

    nominalScale = cloud.projection().nominalScale()

    def _findShadow(cloudHeight):
        cloudHeight = ee.Number(cloudHeight)

        shadowCastedDistance = zenR.tan() \
            .multiply(cloudHeight)

        x = azR.cos().multiply(shadowCastedDistance) \
            .divide(nominalScale).round()

        y = azR.sin().multiply(shadowCastedDistance) \
            .divide(nominalScale).round()

        return cloud.changeProj(cloud.projection(), cloud.projection().translate(x, y))

    shadows = ee.List(cloudHeights).map(_findShadow)

    shadow = ee.ImageCollection.fromImages(shadows).max().unmask()
    shadow = shadow.focal_max(dilatePixels)
    shadow = shadow.And(darkPixels).And(tdomMask.Not().And(cloud.Not()))

    shadowMask = shadow.rename(['cloudShadowTdomMask'])

    return image.addBands(shadowMask)

def getMasks(collection,
             cloudThresh=10,
             zScoreThresh=-1,
             shadowSumThresh=5000,
             dilatePixels=2,
             cloudHeights=[]):
    """"Get cloud and shadow masks.

    Parameters:
        collection (ee.Image): collection TOA or SR containing at least the bands:
            blue, green, red, nir, swir1, swir2 and quality band
        zScoreThresh (int): 
        shadowSumThresh (int): 
        dilatePixels (int): number of pixels to buffering clouds
        cloudFlag (boolean): if True, create a cloud mask using quality band. Defaults to True.
        cloudScore (boolean): if True, create a cloud mask using simple cloud score algorithm. Defaults to True.
        cloudShadowFlag (boolean): if True, create a cloud shadow mask using quality band. Defaults to True.
        cloudShadowTdom (boolean): if True, create a cloud shadow mask using TDOM algorithm. Defaults to True.
        cloudHeights (list): list containing the cloud heights
        cloudBand (str): index band name to be used

    Returns:
        ee.ImageCollection: collection with cloud/shadow masks
    """

    collection = ee.ImageCollection(collection)

    collection = ee.Algorithms.If(
        cloudShadowFlag,
        ee.Algorithms.If(
            cloudShadowTdom,
            tdom(collection.map(cloudShadowFlagMask),
                 zScoreThresh=zScoreThresh,
                 shadowSumThresh=shadowSumThresh,
                 dilatePixels=dilatePixels),
            collection.map(cloudShadowFlagMask)),
        tdom(collection,
             zScoreThresh=zScoreThresh,
             shadowSumThresh=shadowSumThresh,
             dilatePixels=dilatePixels))

    collection = ee.ImageCollection(collection)

    def _getShadowMask(image):

        image = cloudProject(image,
                             shadowSumThresh=shadowSumThresh,
                             dilatePixels=dilatePixels,
                             cloudHeights=cloudHeights,
                             cloudBand=cloudBand)

        return image

    if cloudShadowTdom:
        collection = collection.map(_getShadowMask)

    return collection
