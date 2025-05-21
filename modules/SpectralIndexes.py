#
import ee

# Vegetation and spectral indexes computed from Landsat mosaics
# Assumes input images contain bands: 
# ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']

def getNDVI(image):
    """
    Normalized Difference Vegetation Index (NDVI)
    """

    exp = '( b("nir") - b("red") ) / ( b("nir") + b("red") )'

    ndvi = image.expression(exp)\
        .rename(["ndvi"])\
        .add(1) # Shift to positive range [0, 2]

    return image.addBands(ndvi, overwrite=True)


def getMNDWI(image):
    """
    Modified Normalized Difference Water Index (MNDWI)
    """

    exp = '(b("green") - b("swir1"))/(b("green") + b("swir1"))'

    mndwi = image.expression(exp)\
        .rename(["mndwi"])\
        .add(1)

    return image.addBands(mndwi, overwrite=True)


def getPRI(image):
    """
    Photochemical Reflectance Index (PRI)
    """
    
    exp = '(b("blue") - b("green"))/(b("blue") + b("green"))'

    pri = image.expression(exp)\
        .rename(["pri"])\
        .add(1)

    return image.addBands(pri, overwrite=True)


def getCAI(image):
    """
    Cellulose Absorption Index (CAI)
    """
    exp = '( b("swir2") / b("swir1") )'

    cai = image.expression(exp)\
        .rename(["cai"])\
        .add(1)

    return image.addBands(cai, overwrite=True)


def getEVI2(image):
    """
    Enhanced Vegetation Index 2 (EVI2)
    """

    exp = '2.5 * (b("nir") - b("red")) / (b("nir") + (2.4 * b("red")) + 1)'

    evi2 = image.expression(exp)\
        .rename(["evi2"])\
        .add(1)

    return image.addBands(evi2, overwrite=True)


def getGCVI(image):
    """
    Green Chlorophyll Vegetation Index (GCVI)
    """

    exp = 'b("nir") / b("green") - 1'

    gcvi = image.expression(exp)\
        .rename(["gcvi"])\
        .add(1)

    return image.addBands(gcvi, overwrite=True)


def getGRND(image):
    """
    Green-Red Vegetation Index (GRND)
    """

    exp = '( b("green") - b("red") ) / ( b("green") + b("red") )'

    grnd = image.expression(exp)\
        .rename(["grnd"])\
        .add(1)

    return image.addBands(grnd, overwrite=True)


def getMSI(image):
    """
    Moisture Stress Index (MSI)
    """

    exp = '( b("nir") - b("swir1") ) / ( b("nir") + b("swir1") )'

    msi = image.expression(exp)\
        .rename(["msi"])\
        .add(1)

    return image.addBands(msi, overwrite=True)


def getGARI(image):
    """
    Green Atmospherically Resistant Index (GARI)
    """

    exp = '( b("nir") - (b("green") - (b("blue") - b("red"))) ) / ( b("nir") + (b("green") - (b("blue") - b("red"))) )'

    gari = image.expression(exp)\
        .rename(["gari"])\
        .add(1)

    return image.addBands(gari, overwrite=True)


def getGNDVI(image):
    """
    Green Normalized Difference Vegetation Index (GNDVI)
    """

    exp = '( b("nir") - b("green") ) / ( b("nir") + b("green") )'

    gndvi = image.expression(exp)\
        .rename(["gndvi"])\
        .add(1)

    return image.addBands(gndvi, overwrite=True)


def getMSAVI(image):
    """
    Modified Soil Adjusted Vegetation Index (MSAVI)
    """

    exp = '(2 * b("nir") + 1 - sqrt((2 * b("nir") + 1) ** 2 - 8 * (b("nir") - b("red")))) / 2'
    
    msavi = image.expression(exp)\
        .rename(["msavi"])\
        .add(1)

    return image.addBands(msavi, overwrite=True)


def getNBR(image):
    """
    Normalized Burn Ratio (NBR)
    """

    exp = '( b("nir") - b("swir2") ) / ( b("nir") + b("swir2") )'
    
    nbr = image.expression(exp)\
        .rename(["nbr"])\
        .add(1)

    return image.addBands(nbr, overwrite=True)


def getHallCover(image):
    """
    Hall et al. (2011) Canopy Cover Model
    """

    exp = '( (-b("red") * 0.017) - (b("nir") * 0.007) - (b("swir2") * 0.079) + 5.22 )'

    hallcover = image.expression(exp)\
        .exp()\
        .rename(["hallcover"])

    return image.addBands(hallcover, overwrite=True)


def getHallHeigth(image):
    """
    Hall et al. (2011) Canopy Height Model
    """

    exp = '( (-b("red") * 0.039) - (b("nir") * 0.011) - (b("swir1") * 0.026) + 4.13 )'

    hallheigth = image.expression(exp)\
        .exp()\
        .rename(["hallheigth"])

    return image.addBands(hallheigth, overwrite=True)


def getTGSI(image):
    """
    Tasseled Green Soil Index (TGSI)
    """

    exp = '( b("red") - b("blue") ) / ( b("red") + b("blue") + b("green") )'

    tgsi = image.expression(exp)\
        .exp()\
        .rename(["tgsi"])\
        .add(1)

    return image.addBands(tgsi, overwrite=True)
