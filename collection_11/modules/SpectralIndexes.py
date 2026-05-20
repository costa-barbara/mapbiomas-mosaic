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
        .add(1)

    return image.addBands(ndvi, overwrite=True)


def getEVI2(image):
    """
    Enhanced Vegetation Index 2 (EVI2)
    """

    exp = '2.5 * (b("nir") - b("red")) / (b("nir") + (2.4 * b("red")) + 1)'

    evi2 = image.expression(exp)\
        .rename(["evi2"])\
        .add(1)


    return image.addBands(evi2, overwrite=True)


def getMSAVI(image):
    """
    Modified Soil Adjusted Vegetation Index (MSAVI)
    """

    exp = '(2 * b("nir") + 1 - sqrt((2 * b("nir") + 1) ** 2 - 8 * (b("nir") - b("red")))) / 2'
    
    msavi = image.expression(exp)\
        .rename(["msavi"])\
        .add(1)

    return image.addBands(msavi, overwrite=True)


def getGCVI(image):
    """
    Green Chlorophyll Vegetation Index (GCVI)
    """

    exp = 'b("nir") / b("green") - 1'

    gcvi = image.expression(exp)\
        .rename(["gcvi"])\
        .add(1)

    return image.addBands(gcvi, overwrite=True)


def getMNDWI(image):
    """
    Modified Normalized Difference Water Index (MNDWI)
    """

    exp = '(b("green") - b("swir1"))/(b("green") + b("swir1"))'

    mndwi = image.expression(exp)\
        .rename(["mndwi"])\
        .add(1)

    return image.addBands(mndwi, overwrite=True)


def getNBR(image):
    """
    Normalized Burn Ratio (NBR)
    """

    exp = '(b("nir") - b("swir2")) / (b("nir") + b("swir2"))'

    nbr = image.expression(exp) \
        .rename(["nbr"]) \
        .add(1)

    return image.addBands(nbr, overwrite=True)


def getNDTI(image):
    """
    Normalized Difference Tillage Index (NDTI)

    Uses SWIR1 and SWIR2. Useful for exposed soil, crop residue,
    tillage condition, and agricultural surface differences.
    """

    exp = '(b("swir1") - b("swir2")) / (b("swir1") + b("swir2"))'

    ndti = image.expression(exp) \
        .rename(["ndti"]) \
        .add(1)

    return image.addBands(ndti, overwrite=True)


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


def getMSI(image):
    """
    Moisture Stress Index (MSI)

    Classical MSI formulation: SWIR1 / NIR.
    Higher values generally indicate higher vegetation water stress.
    """

    exp = 'b("swir1") / b("nir")'

    msi = image.expression(exp) \
        .rename(["msi"])

    return image.addBands(msi, overwrite=True)


def getTCW(image):
    """
    Tasseled Cap Wetness (TCW) for Landsat 8/9 OLI-like band names.

    Coefficients from Baig et al. (2014) for Landsat 8 OLI.
    """

    exp = (
        '0.1511 * b("blue") + '
        '0.1973 * b("green") + '
        '0.3283 * b("red") + '
        '0.3407 * b("nir") - '
        '0.7117 * b("swir1") - '
        '0.4559 * b("swir2")'
    )

    tcw = image.expression(exp) \
        .rename(["tcw"])

    return image.addBands(tcw, overwrite=True)


def getTCB(image):
    """
    Tasseled Cap Brightness (TCB) for Landsat 8/9 OLI-like band names.

    Auxiliary component required to compute Tasseled Cap Angle.
    """

    exp = (
        '0.3029 * b("blue") + '
        '0.2786 * b("green") + '
        '0.4733 * b("red") + '
        '0.5599 * b("nir") + '
        '0.5080 * b("swir1") + '
        '0.1872 * b("swir2")'
    )

    tcb = image.expression(exp) \
        .rename(["tcb"])

    return image.addBands(tcb, overwrite=True)


def getTCG(image):
    """
    Tasseled Cap Greenness (TCG) for Landsat 8/9 OLI-like band names.

    Auxiliary component required to compute Tasseled Cap Angle.
    """

    exp = (
        '-0.2941 * b("blue") - '
        '0.2430 * b("green") - '
        '0.5424 * b("red") + '
        '0.7276 * b("nir") + '
        '0.0713 * b("swir1") - '
        '0.1608 * b("swir2")'
    )

    tcg = image.expression(exp) \
        .rename(["tcg"])

    return image.addBands(tcg, overwrite=True)


def getTCA(image):
    """
    Tasseled Cap Angle (TCA)

    Computed as atan(TCG / TCB). It represents the angular relation
    between greenness and brightness.
    """

    image = getTCB(image)
    image = getTCG(image)

    tca = image.expression(
        'atan(b("tcg") / b("tcb"))'
    ).rename(["tca"])

    return image.addBands(tca, overwrite=True)


def getHallCover(image):
    """
    Hall et al. (2011) Canopy Cover Model.

    The Landsat reflectance bands are assumed to be scaled by 10000.
    Therefore, red, nir, and swir2 are divided by 10000 before applying
    the empirical model.
    """

    exp = (
        '((-(b("red") / 10000) * 0.017) - '
        '((b("nir") / 10000) * 0.007) - '
        '((b("swir2") / 10000) * 0.079) + 5.22)'
    )

    hallcover = image.expression(exp) \
        .exp() \
        .rename(["hallcover"])

    return image.addBands(hallcover, overwrite=True)


def getHallHeight(image):
    """
    Hall et al. (2011) Canopy Height Model.

    The Landsat reflectance bands are assumed to be scaled by 10000.
    Therefore, red, nir, and swir1 are divided by 10000 before applying
    the empirical model.
    """

    exp = (
        '((-(b("red") / 10000) * 0.039) - '
        '((b("nir") / 10000) * 0.011) - '
        '((b("swir1") / 10000) * 0.026) + 4.13)'
    )

    hallheight = image.expression(exp) \
        .exp() \
        .rename(["hallheight"])

    return image.addBands(hallheight, overwrite=True)

# --------------------------------------
# SPECIFIC INDEXES FOR ROCKY OUTCROP MAP
# --------------------------------------

def getBSI(image):
    """
    Bare Soil Index.
    Higher values tend to indicate exposed soil / bare substrate.
    """
    bsi = image.expression(
        '((swir1 + red) - (nir + blue)) / ((swir1 + red) + (nir + blue))',
        {
            'blue': image.select('blue'),
            'red': image.select('red'),
            'nir': image.select('nir'),
            'swir1': image.select('swir1')
        }
    ).rename('bsi').toFloat()

    return image.addBands(bsi)


def getNDRI(image):
    """
    Normalized Difference Rock Index / bare rock-oriented SWIR-NIR contrast.
    """
    ndri = image.expression(
        '(swir2 - nir) / (swir2 + nir)',
        {
            'nir': image.select('nir'),
            'swir2': image.select('swir2')
        }
    ).rename('ndri').toFloat()

    return image.addBands(ndri)


# --------------------------------------
# SPECIFIC INDEXES FOR SENTINEL-2 DATA
# --------------------------------------

def getNDVIRED (image):
    """
    Normalized difference vegetation index with red edge band (NDVI Red)
    """
    
    exp = '( b("red_edge_1") - b("red") ) / ( b("red_edge_1") + b("red") )'

    ndviRed = image.expression(exp)\
        .exp()\
        .rename(["ndviRed"])\
        .add(1)

    return image.addBands(ndviRed, overwrite=True)


def getVI700 (image):
    """
    Normalized Difference Chlorophyll Index (NDCI)
    """
    
    exp = '( b("red_edge_1") - b("red_edge_2") ) / ( b("red_edge_1") + b("red_edge_2") )'

    ndci = image.expression(exp)\
        .exp()\
        .rename(["ndci"])\
        .add(1)

    return image.addBands(ndci, overwrite=True)


def getIRECI (image):
    """
    Inverted red-edge chlorophyll index (IRECI)
    """
    
    exp = '( b("red_edge_3") - b("red") ) / ( b("red_edge_1") + b("red_edge_2") )'

    ireci = image.expression(exp)\
        .exp()\
        .rename(["ireci"])\
        .add(1)

    return image.addBands(ireci, overwrite=True)


def getCIRE (image):
    """
    Chlorophyll index red edge (CIRE)
    """
    
    exp = '( b("nir") - b("red_edge_1") )'

    cire = image.expression(exp)\
        .exp()\
        .rename(["cire"])\
        .subtract(1)

    return image.addBands(cire, overwrite=True)


def getTCARI (image):
    """
    Transformed chlorophyll absorption in reflectance index (TCARI)
    """
    exp = '( ((b("red_edge_1") - b("red") ) - 0.2) * ( b("red_edge_1") - b("green") ) ) * (( b("red_edge_1") / b("red") ) * 3)'

    tcari = image.expression(exp)\
        .exp()\
        .rename(["tcari"])\
        .add(1)

    return image.addBands(tcari, overwrite=True)


def getSFDVI (image):
    """
    Spectral feature depth vegetation index (SFDVI)
    """
    exp = '( (( b("green") + b("nir") ) / 2 ) - ( b("red") + b("red_edge_1") ) / 2 )'

    sfdvi = image.expression(exp)\
        .exp()\
        .rename(["sfdvi"])\
        .add(1)

    return image.addBands(sfdvi, overwrite=True)


def getNDRE (image):
    """
    Normalized difference red edge index
    """
    exp = '( b("nir") - b("red_edge_1")) / ( b("nir") + b("red_edge_1")) '

    ndre = image.expression(exp)\
        .exp()\
        .rename(["ndre"])\
        .add(1)

    return image.addBands(ndre, overwrite=True)
  
