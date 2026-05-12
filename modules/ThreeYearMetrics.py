import ee


#--------------------------------
# Reduced three-year temporal metrics
#--------------------------------
def getThreeYearReducedImage(mosaic):
    """
    Keeps only the bands required to compute trailing three-year metrics.

    This avoids storing the full annual mosaic in memory.
    """

    bands = [
        'ndvi_median_wet',
        'ndvi_median_dry',
        'ndfi_median'
    ]

    return mosaic.select(bands).toFloat()


def addThreeYearMetrics(year, mosaic, mosaic_dict_3yr):
    """
    Adds reduced trailing three-year temporal metrics to the current annual mosaic.

    The function uses the current year and up to two previous years.
    Only reduced annual images should be stored in mosaic_dict_3yr.

    Added bands:
        - amp_ndvi_3yr
        - std_ndfi_median_3yr
    """

    current_reduced = getThreeYearReducedImage(mosaic)

    images_3yr = []

    if (year - 2) in mosaic_dict_3yr:
        images_3yr.append(mosaic_dict_3yr[year - 2])

    if (year - 1) in mosaic_dict_3yr:
        images_3yr.append(mosaic_dict_3yr[year - 1])

    images_3yr.append(current_reduced)

    ndvi_wet = ee.ImageCollection.fromImages([
        img.select('ndvi_median_wet') for img in images_3yr
    ])

    ndvi_dry = ee.ImageCollection.fromImages([
        img.select('ndvi_median_dry') for img in images_3yr
    ])

    ndfi_median = ee.ImageCollection.fromImages([
        img.select('ndfi_median') for img in images_3yr
    ])

    amp_ndvi_3yr = ndvi_wet.max() \
        .subtract(ndvi_dry.min()) \
        .rename('amp_ndvi_3yr')

    std_ndfi_median_3yr = ndfi_median.reduce(ee.Reducer.stdDev()) \
        .rename('std_ndfi_median_3yr')

    return mosaic \
        .addBands(amp_ndvi_3yr) \
        .addBands(std_ndfi_median_3yr)

#--------------------------------------
# Temporal metrics for Rocky Outcrop Map
#--------------------------------------

def threeYearMetrics(year, mosaic, mosaic_dict):
    """
    Reduced temporal metrics for rocky outcrop mapping.

    Metrics:
        - mean_bsi_median_3yr: persistence of exposed substrate
        - std_ndvi_median_3yr: interannual vegetation variability
    """

    years_3yr = [y for y in [year - 2, year - 1, year] if y in mosaic_dict]
    mosaics_3yr = [mosaic_dict[y] for y in years_3yr]

    bsi_median = ee.ImageCollection.fromImages([m.select('bsi_median').toFloat() for m in mosaics_3yr])

    ndvi_wet = ee.ImageCollection.fromImages([m.select('ndvi_median_wet').toFloat() for m in mosaics_3yr])

    ndvi_dry = ee.ImageCollection.fromImages([m.select('ndvi_median_dry').toFloat() for m in mosaics_3yr])

    mean_bsi_median_3yr = bsi_median.reduce(ee.Reducer.mean()) \
        .rename('mean_bsi_median_3yr')

    amp_ndvi_3yr = ndvi_wet.max() \
        .subtract(ndvi_dry.min()) \
        .rename('amp_ndvi_3yr')

    return mosaic \
        .addBands(mean_bsi_median_3yr) \
        .addBands(amp_ndvi_3yr)
