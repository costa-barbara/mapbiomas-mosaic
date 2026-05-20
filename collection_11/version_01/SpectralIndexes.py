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
