import ee


def addThreeYearMetrics(year, mosaic, mosaic_dict):
    """
    Adds trailing three-year temporal metrics to the current annual mosaic.

    The function uses the current year and up to two previous years.
    For the first years of the time series, it uses only the available years
    instead of assigning zero-valued bands.

    Metrics are designed to capture:
        - multi-year phenological amplitude
        - interannual variability in vegetation vigor
        - interannual variability in moisture/disturbance-related indices
        - persistence of dry-season vegetation response

    Parameters:
        year (int):
            Target year.

        mosaic (ee.Image):
            Current year's annual mosaic.

        mosaic_dict (dict):
            Dictionary containing annual mosaics already generated for the
            same region, in the format {year: ee.Image}.

    Returns:
        ee.Image:
            Input mosaic with additional three-year temporal metrics.
    """

    # Use current year and up to two previous years.
    years_3yr = [y for y in [year - 2, year - 1, year] if y in mosaic_dict]

    mosaics_3yr = [mosaic_dict[y] for y in years_3yr]

    # Build ImageCollections for selected bands.
    ndvi_wet = ee.ImageCollection.fromImages([m.select('ndvi_median_wet').toFloat() for m in mosaics_3yr])

    ndvi_dry = ee.ImageCollection.fromImages([m.select('ndvi_median_dry').toFloat() for m in mosaics_3yr])

    evi2_wet = ee.ImageCollection.fromImages([m.select('evi2_median_wet').toFloat() for m in mosaics_3yr])

    evi2_dry = ee.ImageCollection.fromImages([m.select('evi2_median_dry').toFloat() for m in mosaics_3yr])

    gcvi_median = ee.ImageCollection.fromImages([m.select('gcvi_median').toFloat() for m in mosaics_3yr])

    nbr_median = ee.ImageCollection.fromImages([m.select('nbr_median').toFloat() for m in mosaics_3yr])

    ndfi_median = ee.ImageCollection.fromImages([m.select('ndfi_median').toFloat() for m in mosaics_3yr])

    ndti_median = ee.ImageCollection.fromImages([m.select('ndti_median').toFloat() for m in mosaics_3yr])

    # Multi-year phenological amplitude.
    # Useful for agriculture and managed pasture, which often show stronger
    # seasonal contrast than native vegetation.
    amp_ndvi_3yr = ndvi_wet.max() \
        .subtract(ndvi_dry.min()) \
        .rename('amp_ndvi_3yr')

    amp_evi2_3yr = evi2_wet.max() \
        .subtract(evi2_dry.min()) \
        .rename('amp_evi2_3yr')

    # Interannual variability of vegetation vigor.
    # Useful for detecting unstable or managed vegetation dynamics.
    std_gcvi_median_3yr = gcvi_median.reduce(ee.Reducer.stdDev()) \
        .rename('std_gcvi_median_3yr')

    # Interannual variability of disturbance/moisture-related response.
    std_nbr_median_3yr = nbr_median.reduce(ee.Reducer.stdDev()) \
        .rename('std_nbr_median_3yr')

    # Interannual variability of vegetation structure/integrity.
    std_ndfi_median_3yr = ndfi_median.reduce(ee.Reducer.stdDev()) \
        .rename('std_ndfi_median_3yr')

    # Mean NDTI across three years.
    # Useful for persistent agricultural soil/residue/tillage signal.
    mean_ndti_median_3yr = ndti_median.reduce(ee.Reducer.mean()) \
        .rename('mean_ndti_median_3yr')

    return mosaic \
        .addBands(amp_ndvi_3yr) \
        .addBands(amp_evi2_3yr) \
        .addBands(std_gcvi_median_3yr) \
        .addBands(std_nbr_median_3yr) \
        .addBands(std_ndfi_median_3yr) \
        .addBands(mean_ndti_median_3yr)
