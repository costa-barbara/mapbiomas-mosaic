import ee

def addThreeYearMetrics(year, mosaic, mosaic_dict, aoi_mask):
    """
    Adds three-year metrics related to NDVI and NBR to the given mosaic.

    Parameters:
        year (int): The target year to compute metrics for.
        mosaic (ee.Image): The current year's mosaic.
        mosaic_dict (dict): Dictionary of mosaics for all years {year: ee.Image}.
        aoi_mask (ee.Image): Binary mask (1 = valid pixel, 0 = masked) for the analysis area.

    Returns:
        ee.Image: Mosaic with added bands:
                  - amp_ndvi_3yr: NDVI amplitude over 3 years (wet - dry).
                  - var_ndvi_p25_3yr: Variance of NDVI P25 over 3 years.
                  - var_nbr_median_3yr: Variance of NBR median over 3 years.
    """

    if year < min(mosaic_dict.keys()) + 2:
        # If there are not enough previous years to compute 3-year metrics
        amp_ndvi_3yr = ee.Image(0).rename('amp_ndvi_3yr').updateMask(aoi_mask.eq(1))
        var_ndvi_p25_3yr = ee.Image(0).rename('var_ndvi_p25_3yr').updateMask(aoi_mask.eq(1))
        var_nbr_median_3yr = ee.Image(0).rename('var_nbr_median_3yr').updateMask(aoi_mask.eq(1))
    else:
        # Get the mosaics from the current and two previous years
        mosaics_3yr = [
            mosaic_dict[year],
            mosaic_dict[year - 1],
            mosaic_dict[year - 2]
        ]

        # Compute NDVI amplitude: max(ndvi_median_wet) - min(ndvi_median_dry)
        min_ndvi_dry = ee.ImageCollection.fromImages([m.select('ndvi_median_dry').toFloat() for m in mosaics_3yr]).min()
        max_ndvi_wet = ee.ImageCollection.fromImages([m.select('ndvi_median_wet').toFloat() for m in mosaics_3yr]).max()
        amp_ndvi_3yr = max_ndvi_wet.subtract(min_ndvi_dry)\
            .rename('amp_ndvi_3yr')\
            .updateMask(aoi_mask.eq(1))

        # Compute variance of NDVI P25 over 3 years
        ndvi_p25_stack = ee.ImageCollection.fromImages([m.select('ndvi_p25') for m in mosaics_3yr])
        mean_p25 = ndvi_p25_stack.reduce(ee.Reducer.mean())
        var_ndvi_p25_3yr = ndvi_p25_stack.map(lambda img: img.subtract(mean_p25).pow(2))\
            .reduce(ee.Reducer.mean())\
            .rename('var_ndvi_p25_3yr')\
            .updateMask(aoi_mask.eq(1))

        # Compute variance of NBR median over 3 years
        nbr_stack = ee.ImageCollection.fromImages([m.select('nbr_median') for m in mosaics_3yr])
        mean_nbr = nbr_stack.reduce(ee.Reducer.mean())
        var_nbr_median_3yr = nbr_stack.map(lambda img: img.subtract(mean_nbr).pow(2))\
            .reduce(ee.Reducer.mean())\
            .rename('var_nbr_median_3yr')\
            .updateMask(aoi_mask.eq(1))

    # Add all metrics to the original mosaic
    return mosaic.addBands(amp_ndvi_3yr)\
                 .addBands(var_ndvi_p25_3yr)\
                 .addBands(var_nbr_median_3yr)
