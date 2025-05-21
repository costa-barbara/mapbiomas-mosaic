import ee
import math
#
#
#
# Calculates terrain slope (in %) from the MERIT DEM and adds it as a new band to the input image
def getSlope(image):
    """
    Adds a slope band (percent) to the input image, derived from the MERIT DEM.

    Parameters:
        image (ee.Image): The image to which the slope band will be added.

    Returns:
        ee.Image: Input image with an additional 'slope' band in percent.
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

#
#
#
# Computes entropy texture on the green band to assess spatial variation in vegetation or brightness
def getEntropyG(image):
    """
    Computes entropy texture on the green band using a 5-pixel square kernel.
    Intended for use with Landsat monthly mosaics that include 'green_median'.

    Parameters:
        image (ee.Image): Image containing the 'green_median' band.

    Returns:
        ee.Image: Input image with an additional 'green_median_texture' band (0–100).
    """
    square = ee.Kernel.square(radius=5)

    entropyG = image.select('green_median')\
        .int32()\
        .entropy(square)\
        .multiply(100)\
        .rename("green_median_texture")

    return image.addBands(entropyG)
