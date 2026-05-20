#
import ee

def getNDVI(image):

    exp = '( b("nir") - b("red") ) / ( b("nir") + b("red") )'

    ndvi = image.expression(exp)\
        .rename(["ndvi"])\
        .add(1)

    return image.addBands(srcImg=ndvi, overwrite=True)


def getMNDWI(image):

    exp = '(b("green") - b("swir1"))/(b("green") + b("swir1"))'

    mndwi = image.expression(exp)\
        .rename(["mndwi"])\
        .add(1)

    return image.addBands(srcImg=mndwi, overwrite=True)


def getPRI(image):

    exp = '(b("blue") - b("green"))/(b("blue") + b("green"))'

    pri = image.expression(exp)\
        .rename(["pri"])\
        .add(1)

    return image.addBands(srcImg=pri, overwrite=True)


def getCAI(image):

    exp = '( b("swir2") / b("swir1") )'

    cai = image.expression(exp)\
        .rename(["cai"])\
        .add(1)

    return image.addBands(srcImg=cai, overwrite=True)


def getEVI2(image):

    exp = '2.5 * (b("nir") - b("red")) / (b("nir") + (2.4 * b("red")) + 1)'

    evi2 = image.expression(exp)\
        .rename(["evi2"])\
        .add(1)

    return image.addBands(srcImg=evi2, overwrite=True)


def getGCVI(image):

    exp = 'b("nir") / b("green") - 1'

    gcvi = image.expression(exp)\
        .rename(["gcvi"])\
        .add(1)

    return image.addBands(gcvi)


def getGRND(image):

    exp = '( b("green") - b("red") ) / ( b("green") + b("red") )'

    grnd = image.expression(exp)\
        .rename(["grnd"])\
        .add(1)

    return image.addBands(grnd)


def getMSI(image):

    exp = '( b("nir") - b("swir1") ) / ( b("nir") + b("swir1") )'

    msi = image.expression(exp)\
        .rename(["msi"])\
        .add(1)

    return image.addBands(msi)


def getGARI(image):

    exp = '( b("nir") - (b("green") - (b("blue") - b("red"))) ) / ( b("nir") + (b("green") - (b("blue") - b("red"))) )'

    gari = image.expression(exp)\
        .rename(["gari"])\
        .add(1)

    return image.addBands(gari)


def getGNDVI(image):

    exp = '( b("nir") - b("green") ) / ( b("nir") + b("green") )'

    gndvi = image.expression(exp)\
        .rename(["gndvi"])\
        .add(1)

    return image.addBands(gndvi)


def getMSAVI(image):

    exp = '(2 * b("nir") + 1 - sqrt((2 * b("nir") + 1) ** 2 - 8 * (b("nir") - b("red")))) / 2'
    
    msavi = image.expression(exp)\
        .rename(["msavi"])\
        .add(1)

    return image.addBands(msavi)


def getNBR(image):

    exp = '( b("nir") - b("swir2") ) / ( b("nir") + b("swir2") )'
    
    nbr = image.expression(exp)\
        .rename(["nbr"])\
        .add(1)

    return image.addBands(nbr)


def getHallCover(image):

    exp = '( (-b("red") * 0.017) - (b("nir") * 0.007) - (b("swir2") * 0.079) + 5.22 )'

    hallcover = image.expression(exp)\
        .exp()\
        .rename(["hallcover"])

    return image.addBands(hallcover)


def getHallHeigth(image):

    exp = '( (-b("red") * 0.039) - (b("nir") * 0.011) - (b("swir1") * 0.026) + 4.13 )'

    hallheigth = image.expression(exp)\
        .exp()\
        .rename(["hallheigth"])

    return image.addBands(hallheigth)


def getTGSI(image):

    exp = '( b("red") - b("blue") ) / ( b("red") + b("blue") + b("green") )'

    tgsi = image.expression(exp)\
        .exp()\
        .rename(["tgsi"])\
        .add(1)

    return image.addBands(tgsi)
    
#--------------------------------------
# Specific indexes for Sentinel-2 data
#--------------------------------------

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
    exp = '( (b("red_edge_1") - b("red") ) - 0.2 * ( b("red_edge_1") - b("green") ) ) * ( b("red_edge_1") / b("red") ) * 3'

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
