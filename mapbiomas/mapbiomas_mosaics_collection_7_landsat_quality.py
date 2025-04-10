# -*- coding: utf-8 -*-

import ee
import sys
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('../'))

from modules.Collection import *
from modules.BandNames import *
from modules.CloudAndShadowMaskC2 import *

# Initialize
ee.Initialize(project="mapbiomas")

assetMasks = "projects/mapbiomas-workspace/AUXILIAR/landsat-mask"
assetOutput = 'projects/mapbiomas-workspace/COLECAO7/qualidade'

years = [
    2023,
    # 2022,
    # 2021,
    # 2020,
    # 2019, 
    # 2018,
    # 2017, 
    # 2016, 
    # 2015,
    # 2014, 
    # 2013, 
    # 2012,
    # 2011, 
    # 2010, 
    # 2009,
    # 2008, 
    # 2007, 
    # 2006,
    # 2005, 
    # 2004, 
    # 2003,
    # 2002, 
    # 2001, 
    # 2000,
    # 1999, 
    # 1998, 
    # 1997,
    # 1996, 
    # 1995, 
    # 1994,
    # 1993, 
    # 1992, 
    # 1991,
    # 1990, 
    # 1989, 
    # 1988,
    # 1987, 
    # 1986, 
    # 1985
]

# america do sul
tilesRegions = ee.Geometry.Polygon(
    [
        [
            [-94.28945710207519, 16.16381488543265],
            [-94.28945710207519, -57.63846532620302],
            [-31.97500397707519, -57.63846532620302],
            [-31.97500397707519, 16.16381488543265]
        ]
    ], None, False)

tiles = (
    ee.ImageCollection(assetMasks)
    .filterMetadata('version', 'equals', '2')
    .filter(ee.Filter.bounds(tilesRegions))
)

tileIds = tiles.reduceColumns(
    ee.Reducer.toList(), ['tile']).get('list').getInfo()


for year in years:

    outputCollection = ee.ImageCollection(assetOutput)\
        .filterMetadata('year', 'equals', year)

    imageNames = outputCollection\
        .reduceColumns(ee.Reducer.toList(), ['system:index'])\
        .get('list')\
        .getInfo()

    for tileId in tileIds:
        name = '{}-{}'.format(tileId, year)

        print(name)

        if name not in imageNames:
            try:
                tileMask = ee.Image(tiles.filterMetadata(
                    'tile', 'equals', tileId).first())

                centroid = tileMask\
                    .geometry()\
                    .centroid()

                collection = ee.ImageCollection([])

                # returns a collection containing the specified parameters
                collectionL5 = getCollection(
                    collectionId='LANDSAT/LT05/C02/T1_L2',
                    dateStart=str(year)+'-01-01',
                    dateEnd=str(year)+'-12-31',
                    cloudCover=100,
                    geometry=centroid
                )

                # returns a collection containing the specified parameters
                collectionL7 = getCollection(
                    collectionId='LANDSAT/LE07/C02/T1_L2',
                    dateStart=str(year)+'-01-01',
                    dateEnd=str(year)+'-12-31',
                    cloudCover=100,
                    geometry=centroid
                )

                # returns a collection containing the specified parameters
                collectionL8 = getCollection(
                    collectionId='LANDSAT/LC08/C02/T1_L2',
                    dateStart=str(year)+'-01-01',
                    dateEnd=str(year)+'-12-31',
                    cloudCover=100,
                    geometry=centroid
                )

                # returns a collection containing the specified parameters
                collectionL9 = getCollection(
                    collectionId='LANDSAT/LC09/C02/T1_L2',
                    dateStart=str(year)+'-01-01',
                    dateEnd=str(year)+'-12-31',
                    cloudCover=100,
                    geometry=centroid
                )

                # returns  a pattern of band names
                bands = getBandNames('l5c2')

                # Rename collection image bands
                collectionL5 = collectionL5.select(
                    bands['bandNames'],
                    bands['newNames']
                )

                # Get cloud and shadow masks
                collectionWithMasksL5 = getMasks(
                    collectionL5,
                    cloudFlag=True,
                    cloudScore=True,
                    cloudShadowFlag=True,
                    cloudShadowTdom=True,
                    zScoreThresh=-1,
                    shadowSumThresh=4000,
                    dilatePixels=2,
                    cloudHeights=ee.List.sequence(200, 10000, 500),
                    cloudBand='cloudFlagMask'
                )

                collection = collection.merge(collectionWithMasksL5)

                # returns  a pattern of band names
                bands = getBandNames('l7c2')

                # Rename collection image bands
                collectionL7 = collectionL7.select(
                    bands['bandNames'],
                    bands['newNames']
                )

                # Get cloud and shadow masks
                collectionWithMasksL7 = getMasks(
                    collectionL7,
                    cloudFlag=True,
                    cloudScore=True,
                    cloudShadowFlag=True,
                    cloudShadowTdom=True,
                    zScoreThresh=-1,
                    shadowSumThresh=4000,
                    dilatePixels=2,
                    cloudHeights=ee.List.sequence(200, 10000, 500),
                    cloudBand='cloudFlagMask'
                )

                collection = collection.merge(collectionWithMasksL7)

                # returns  a pattern of band names
                bands = getBandNames('l8c2')

                # Rename collection image bands
                collectionL8 = collectionL8.select(
                    bands['bandNames'],
                    bands['newNames']
                )

                # Get cloud and shadow masks
                collectionWithMasksL8 = getMasks(
                    collectionL8,
                    cloudFlag=True,
                    cloudScore=True,
                    cloudShadowFlag=True,
                    cloudShadowTdom=True,
                    zScoreThresh=-1,
                    shadowSumThresh=4000,
                    dilatePixels=2,
                    cloudHeights=ee.List.sequence(200, 10000, 500),
                    cloudBand='cloudFlagMask'
                )

                collection = collection.merge(collectionWithMasksL8)

                # returns  a pattern of band names
                bands = getBandNames('l9c2')

                # Rename collection image bands
                collectionL9 = collectionL9.select(
                    bands['bandNames'],
                    bands['newNames']
                )

                # Get cloud and shadow masks
                collectionWithMasksL9 = getMasks(
                    collectionL9,
                    cloudFlag=True,
                    cloudScore=True,
                    cloudShadowFlag=True,
                    cloudShadowTdom=True,
                    zScoreThresh=-1,
                    shadowSumThresh=4000,
                    dilatePixels=2,
                    cloudHeights=ee.List.sequence(200, 10000, 500),
                    cloudBand='cloudFlagMask'
                )

                collection = collection.merge(collectionWithMasksL9)
                # print(collection.size().getInfo())

                # collection = collectionWithMasksL5.merge(
                #     collectionWithMasksL7).merge(collectionWithMasksL8)

                quality = collection.map(
                    lambda image: image.select('cloudFlagMask').Not()
                )

                quality = quality \
                    .reduce(ee.Reducer.sum()) \
                    .rename('quality')

                quality = quality.mask(tileMask)

                geometry = tileMask.geometry()

                task = ee.batch.Export.image.toAsset(
                    image=quality.toByte().set('year', year),
                    description=name,
                    assetId='{}/{}'.format(assetOutput, name),
                    pyramidingPolicy={".default": "mode"},
                    region=geometry.getInfo()['coordinates'],
                    scale=30,
                )

                task.start()
            except Exception as e:
                print(e)
