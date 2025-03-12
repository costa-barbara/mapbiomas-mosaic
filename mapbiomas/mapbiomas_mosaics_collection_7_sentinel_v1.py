from pprint import pprint
import ee
import sys
import os

sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('../'))

from modules.Mosaic import *
from modules.DataType import *
from modules.BandNames import *
from modules.Collection import *
from modules.SmaAndNdfi import *
from modules.Miscellaneous import *
from modules.SpectralIndexes import *
from modules.CloudAndShadowMaskS2 import *

ee.Initialize()

ASSET_GRIDS = 'projects/mapbiomas-workspace/AUXILIAR/cartas'

ASSET_ORBITS = 'projects/mapbiomas-workspace/AUXILIAR/sentinel-2-orbit'

# nome do bioma sem espaço
biomeNames = [
    # 'CAATINGA',
    # 'PAMPA',
#     'PANTANAL',
#     'MATAATLANTICA',
#     'CERRADO',
    'AMAZONIA'
]

version = {
    'AMAZONIA': '3',
    'CAATINGA': '3',
    'CERRADO': '3',
    'MATAATLANTICA': '3',
    'PAMPA': '3',
    'PANTANAL': '3',
}

CLOUD_PROBABILITY = {
    'CAATINGA': 15,
    'CERRADO': 40,
    'MATAATLANTICA': 40,
    'PAMPA': 40,
    'PANTANAL': 40,
    'AMAZONIA': 30,
}

dataFilter = {
    'CAATINGA': {
        'dateStart': '01-01',
        'dateEnd': '07-31',
        'cloudCover': 80
    },
    'CERRADO': {
        'dateStart': '04-01',
        'dateEnd': '09-30',
        'cloudCover': 50
    },
    'MATAATLANTICA': {
        'dateStart': '03-01',
        'dateEnd': '10-31',
        'cloudCover': 80
    },
    'PAMPA': {
        'dateStart': '09-01',
        'dateEnd': '11-30',
        'cloudCover': 90
    },
    'PANTANAL': {
        'dateStart': '03-01',
        'dateEnd': '10-31',
        'cloudCover': 90
    },
    'AMAZONIA': {
        'dateStart': '06-01',
        'dateEnd': '10-31',
        'cloudCover': 50
    },
}

gridNames = {
    "AMAZONIA": [
        "SC-20-Y-B", "SC-21-Y-A", "SC-21-Y-B", "SC-21-Y-C",
        "SC-21-Y-D", "SC-21-Z-A", "SC-21-Z-B", "SC-21-Z-D",
        "SB-22-V-B", "SA-22-Z-A", "SA-22-Z-C", "SA-22-X-C",
        "SA-22-X-D", "SA-23-V-C", "SA-23-Y-A", "SA-23-Y-C",
        "SB-23-V-D", "SB-23-X-A", "SB-23-V-B", "SA-23-Y-D",
        "SA-23-Z-C", "SA-23-Z-B", "SA-23-X-C", "SA-23-Z-A",
        "SA-23-Y-B", "SA-23-V-D", "SA-23-V-B", "NB-22-Y-D",
        "NA-22-V-B", "NA-22-X-A", "NA-22-X-C", "NA-22-Z-A",
        "SA-23-V-A", "NA-22-Z-D", "SA-22-X-B", "NA-22-Z-C",
        "SA-22-X-A", "NA-22-Y-D", "SA-22-V-B", "SA-22-V-A",
        "NA-22-Y-C", "NA-22-Y-B", "NA-22-Y-A", "NA-22-V-D",
        "NA-22-V-C", "NA-21-Z-B", "NA-21-X-D", "NA-21-Z-D",
        "SA-21-X-B", "SA-21-X-A", "NA-21-Z-C", "NA-21-Z-A",
        "NA-21-X-C", "NA-21-Y-B", "NA-21-V-D", "NA-21-Y-D",
        "SA-21-V-B", "SA-21-V-A", "NA-21-Y-C", "NA-21-Y-A",
        "SA-20-X-B", "NA-20-Z-D", "NA-20-Z-B", "NA-20-X-D",
        "NA-21-V-C", "NA-21-V-A", "NA-20-X-B", "NB-20-Z-D",
        "NB-21-Y-C", "NB-20-Z-B", "NB-21-Y-A", "NB-20-Z-C",
        "NB-20-Y-D", "NB-20-Y-C", "NA-20-V-A", "NA-19-X-D",
        "NA-20-V-D", "NA-20-V-B", "NA-20-X-A", "NA-20-X-C",
        "NA-20-Y-B", "NA-20-Z-A", "NA-20-Z-C", "SA-20-X-A",
        "SA-20-V-B", "NA-20-Y-D", "SA-20-V-A", "NA-20-Y-C",
        "NA-20-Y-A", "NA-19-Z-B", "NA-19-Z-D", "SA-19-X-B",
        "SA-19-X-A", "NA-19-Z-C", "NA-19-Z-A", "SA-19-V-B",
        "NA-19-Y-D", "NA-19-Y-B", "NA-19-X-C", "SC-19-Y-D",
        "SC-19-Y-A", "SC-19-Y-B", "SC-19-V-D", "SC-19-Z-A",
        "SC-19-X-C", "SC-19-Z-C", "SC-19-Z-B", "SC-19-X-D",
        "SC-19-X-B", "SC-19-X-A", "SC-19-V-B", "SB-19-Z-C",
        "SB-19-Y-D", "SB-19-Z-D", "SB-19-Z-A", "SB-19-Z-B",
        "SB-19-X-C", "SB-19-X-D", "SB-19-X-A", "SB-19-X-B",
        "SB-19-Y-B", "SB-19-V-D", "SB-19-V-B", "SB-19-Y-C",
        "SB-19-Y-A", "SB-19-V-C", "SB-19-V-A", "SB-18-Z-B",
        "SB-18-X-D", "SB-18-X-B", "SB-18-Z-D", "SC-18-X-B",
        "SC-19-V-A", "SC-19-V-C", "SC-18-X-D", "SC-18-X-A",
        "SB-18-Z-C", "SB-18-Z-A", "SA-19-V-D", "SA-19-Y-B",
        "SA-19-Y-D", "SA-19-Z-A", "SA-19-Z-C", "SA-19-Z-D",
        "SA-19-Z-B", "SA-19-X-D", "SA-19-X-C", "SA-20-V-C",
        "SA-20-Y-A", "SA-20-Y-B", "SA-20-V-D", "SA-20-X-C",
        "SA-20-X-D", "SA-20-Z-A", "SA-20-Z-B", "SA-20-Y-D",
        "SA-20-Z-C", "SA-20-Z-D", "SB-20-X-A", "SB-20-X-B",
        "SB-20-V-B", "SB-20-V-A", "SA-20-Y-C", "SB-20-V-C",
        "SB-20-V-D", "SB-20-Y-A", "SB-20-Y-B", "SB-20-Y-D",
        "SB-20-Y-C", "SC-20-V-A", "SC-20-V-C", "SC-20-V-D",
        "SC-20-V-B", "SB-20-Z-A", "SB-20-Z-C", "SC-20-X-A",
        "SC-20-X-C", "SC-20-X-D", "SC-20-X-B", "SB-20-Z-D",
        "SB-20-Z-B", "SB-20-X-C", "SB-20-X-D", "SB-21-V-C",
        "SB-21-V-A", "SB-21-V-B", "SB-21-V-D", "SB-21-Y-A",
        "SB-21-Y-B", "SB-21-Y-C", "SC-21-V-C", "SC-21-V-A",
        "SC-21-V-B", "SC-21-V-D", "SB-21-Y-D", "SB-21-Z-A",
        "SB-21-Z-C", "SC-21-X-A", "SC-21-X-B", "SB-21-Z-D",
        "SB-21-Z-B", "SB-21-X-C", "SB-21-X-D", "SB-21-X-A",
        "SB-21-X-B", "SA-21-Z-C", "SA-21-Z-D", "SA-21-Z-B",
        "SA-21-Z-A", "SA-21-Y-D", "SA-21-Y-B", "SA-21-Y-C",
        "SA-21-Y-A", "SA-21-V-D", "SA-21-V-C", "SA-21-X-C",
        "SA-21-X-D", "SA-22-V-C", "SB-22-V-A", "SA-22-Y-C",
        "SA-22-Y-A", "SA-22-V-D", "SA-22-Y-B", "SA-22-Y-D",
        "SB-22-V-B", "SA-22-Z-A", "SA-22-Z-C", "SA-22-X-C",
        "SA-22-X-D", "SA-23-V-C", "SA-23-Y-A", "SA-23-Y-C",
        "SA-22-Z-D", "SA-22-Z-B", "SB-22-X-A", "SB-22-X-B",
        "SB-22-X-C", "SB-22-X-D", "SB-23-V-C", "SB-23-V-A",
        "SB-23-Y-A", "SB-22-Z-D", "SC-22-X-B", "SB-22-Z-B",
        "SB-22-Z-A", "SB-22-Z-C", "SC-22-X-A", "SB-22-Y-D",
        "SC-22-V-B", "SC-22-V-A", "SB-22-Y-C", "SB-22-Y-B",
        "SB-22-Y-A", "SB-22-V-D", "SB-22-V-C", "SC-21-X-D",
        "SC-22-V-C", "SC-22-Y-A", "SC-21-Z-B", "SC-22-Y-C",
        "SC-21-Z-D", "SD-21-X-B", "SD-21-X-D", "SD-22-V-A",
        "SD-22-V-C", "SC-22-Y-B", "SC-22-Y-D", "SD-22-V-B",
        "SD-22-V-D", "SC-22-Z-A", "SC-22-X-C", "SC-22-V-D",
        "SC-22-X-D", "SE-21-V-B", "SE-21-V-A", "SD-21-Y-C",
        "SD-21-Y-D", "SE-20-X-B", "SD-20-Z-D", "SD-20-Z-B",
        "SD-21-Y-A", "SD-21-Y-B", "SD-21-V-D", "SD-21-X-C",
        "SD-21-Z-A", "SD-21-Z-C", "SD-21-X-A", "SD-21-V-B",
        "SC-21-Y-D", "SC-21-Z-C", "SC-21-Z-A", "SC-21-X-C",
        "SC-21-Y-B", "SC-21-Y-C", "SC-21-Y-A", "SC-20-Z-B",
        "SC-20-Z-D", "SD-20-X-B", "SD-20-X-D", "SD-21-V-A",
        "SD-21-V-C", "SD-20-X-C", "SD-20-V-B", "SD-20-X-A",
        "SC-20-Z-C", "SC-20-Z-A", "SC-20-Y-B", "SC-20-Y-D",
        "SD-20-V-A", "SC-20-Y-C", "SC-20-Y-A"
    ],
    "CERRADO": [
        "SF-23-V-D", "SF-23-X-A", "SF-23-V-B", "SE-23-Y-D",
        "SE-23-Z-C", "SE-23-Z-D", "SE-23-Z-A", "SE-23-Y-B",
        "SE-23-X-C", "SE-23-V-D", "SE-23-V-B", "SE-23-X-A",
        "SE-23-X-D", "SE-23-Z-B", "SE-23-X-B", "SD-23-X-B",
        "SD-23-X-D", "SD-24-Y-A", "SD-23-Z-B", "SD-24-Y-C",
        "SE-24-V-A", "SD-23-Z-D", "SD-23-Z-A", "SD-23-Z-C",
        "SD-23-Y-D", "SD-23-Y-B", "SD-23-X-C", "SD-23-V-D",
        "SD-23-V-B", "SD-23-X-A", "SC-23-Z-C", "SC-23-Y-D",
        "SC-23-Z-A", "SC-23-Y-B", "SC-23-X-C", "SC-23-V-D",
        "SB-23-Z-D", "SB-23-Z-C", "SC-23-X-A", "SC-23-V-B",
        "SB-23-Y-D", "SB-23-Y-B", "SB-23-Z-A", "SB-23-Z-B",
        "SB-23-X-D", "SB-23-X-C", "SB-23-V-D", "SB-23-X-A",
        "SB-23-V-B", "SA-23-Z-C", "SB-23-X-B", "SA-23-Z-D",
        "SB-24-V-C", "SB-24-V-A", "SA-24-Y-C", "SB-24-Y-A",
        "SA-24-Y-A", "SA-23-Z-B", "SA-23-Z-A", "SB-22-X-D",
        "SB-23-V-C", "SB-23-Y-A", "SB-23-Y-C", "SB-22-Z-D",
        "SC-22-X-B", "SB-22-Z-B", "SB-22-Z-C", "SC-22-X-A",
        "SD-21-X-B", "SD-21-X-D", "SD-22-V-C", "SC-22-Y-B",
        "SC-22-Y-D", "SD-22-V-B", "SD-22-V-D", "SC-22-Z-C",
        "SD-22-X-A", "SC-22-Z-A", "SC-22-X-C", "SC-22-X-D",
        "SC-22-Z-B", "SC-23-V-C", "SC-23-Y-A", "SC-23-V-A",
        "SC-23-Y-C", "SD-23-V-A", "SD-22-X-B", "SC-22-Z-D",
        "SD-22-X-C", "SD-22-X-D", "SD-22-Z-A", "SD-22-Z-B",
        "SD-22-Z-C", "SD-22-Z-D", "SD-23-Y-A", "SD-23-V-C",
        "SD-23-Y-C", "SE-23-V-A", "SE-23-V-C", "SE-22-X-B",
        "SE-22-X-D", "SE-22-X-A", "SE-22-X-C", "SE-22-V-D",
        "SE-22-V-B", "SE-22-Y-B", "SE-22-Y-A", "SE-22-V-C",
        "SE-22-V-A", "SD-22-Y-D", "SD-22-Y-C", "SD-22-Y-B",
        "SD-22-Y-A", "SE-21-X-B", "SD-21-Z-D", "SD-21-Z-B",
        "SE-21-X-D", "SE-21-Z-B", "SE-21-Z-C", "SE-21-X-A",
        "SE-21-V-B", "SE-21-Y-D", "SD-21-Y-C", "SD-21-Y-D",
        "SD-21-Y-A", "SD-21-Y-B", "SD-21-V-D", "SD-21-X-C",
        "SD-21-Z-A", "SD-21-Z-C", "SD-21-X-A", "SD-21-V-B",
        "SC-21-Y-D", "SC-21-Y-C", "SD-20-X-B", "SD-21-V-A",
        "SD-21-V-C", "SG-21-X-B", "SF-21-Z-C", "SF-21-Z-D",
        "SF-21-Z-A", "SF-21-Z-B", "SF-21-X-C", "SF-21-X-D",
        "SF-21-Y-B", "SF-21-V-D", "SF-21-V-B", "SF-21-X-A",
        "SF-21-X-B", "SE-21-Z-D", "SE-22-Y-C", "SF-22-V-A",
        "SF-22-V-C", "SF-22-Y-A", "SF-22-V-D", "SF-22-V-B",
        "SF-22-Y-B", "SF-22-Z-A", "SF-22-Z-C", "SF-22-X-A",
        "SE-22-Z-C", "SE-22-Z-A", "SE-22-Y-D", "SE-22-Z-B",
        "SE-22-Z-D", "SF-22-X-B", "SE-23-Y-A", "SE-23-Y-C",
        "SF-23-V-A", "SF-23-V-C", "SF-23-Y-A", "SF-22-X-D",
        "SF-22-Z-B", "SF-22-Z-D", "SG-22-X-A", "SG-22-X-B",
        "SF-23-Y-C"
    ],
    "CAATINGA": [
        "SE-23-V-B", "SE-23-X-A", "SE-23-X-B", "SB-25-V-C",
        "SB-25-Y-A", "SB-25-Y-C", "SC-25-V-A", "SC-24-X-D",
        "SC-24-Z-B", "SC-24-X-B", "SC-24-X-A", "SC-24-X-C",
        "SC-24-V-B", "SC-24-V-D", "SC-24-Z-A", "SC-24-Y-B",
        "SC-24-Z-C", "SD-24-X-A", "SC-24-Y-D", "SD-24-V-B",
        "SD-24-Y-B", "SD-24-V-D", "SD-24-V-A", "SD-24-V-C",
        "SD-23-X-B", "SD-23-X-D", "SD-24-Y-A", "SD-23-Z-B",
        "SD-24-Y-C", "SD-23-Z-D", "SD-23-Z-A", "SD-23-Z-C",
        "SD-23-Y-D", "SD-23-X-C", "SD-23-X-A", "SC-23-Z-C",
        "SC-23-Z-A", "SC-23-X-C", "SC-23-Z-B", "SC-23-Z-D",
        "SC-23-X-D", "SC-24-Y-C", "SC-24-Y-A", "SC-24-V-C",
        "SC-23-X-B", "SC-24-V-A", "SB-24-Y-C", "SB-23-Z-D",
        "SB-23-Z-C", "SC-23-X-A", "SB-23-Z-B", "SB-24-V-C",
        "SB-24-V-A", "SA-24-Y-C", "SB-24-V-B", "SA-24-Y-D",
        "SB-24-V-D", "SB-24-Y-A", "SB-24-Y-B", "SB-24-Y-D",
        "SB-24-Z-C", "SB-24-Z-A", "SB-24-Z-B", "SB-24-Z-D",
        "SB-24-X-D", "SB-24-X-B", "SB-24-X-A", "SA-24-Z-C",
        "SB-24-X-C", "SA-24-Y-B", "SA-24-Y-A"
    ],
    "MATAATLANTICA": [
        "SG-23-V-B", "SF-23-Y-D", "SF-23-Z-C", "SF-24-Y-C",
        "SF-23-Z-D", "SF-24-Y-A", "SF-23-Z-B", "SF-23-X-D",
        "SF-23-X-C", "SF-23-Z-A", "SF-23-Y-B", "SF-23-V-D",
        "SF-23-X-A", "SF-23-V-B", "SE-23-Y-D", "SE-23-Z-C",
        "SF-23-X-B", "SE-23-Z-D", "SE-23-Z-A", "SE-23-X-D",
        "SE-23-Z-B", "SE-23-X-B", "SE-24-Y-C", "SE-24-Y-A",
        "SE-24-V-C", "SE-24-Y-B", "SE-24-V-D", "SE-24-Y-D",
        "SF-24-V-A", "SF-24-V-B", "SF-24-V-C", "SB-25-V-C",
        "SB-25-Y-A", "SB-25-Y-C", "SC-25-V-A", "SC-25-V-C",
        "SC-24-X-D", "SC-24-Z-B", "SC-24-Z-D", "SC-24-X-B",
        "SC-24-Z-A", "SC-24-Z-C", "SD-24-X-A", "SC-24-Y-D",
        "SD-24-V-B", "SD-24-X-C", "SD-24-Z-C", "SE-24-X-A",
        "SE-24-V-B", "SD-24-Y-D", "SD-24-Y-B", "SD-24-Z-A",
        "SD-24-V-D", "SD-24-V-C", "SD-24-Y-A", "SD-24-Y-C",
        "SE-24-V-A", "SD-23-Z-D", "SE-22-X-D", "SE-22-Y-B",
        "SH-21-X-D", "SH-21-X-B", "SG-21-Z-D", "SG-21-X-D",
        "SG-21-X-B", "SF-21-Z-D", "SF-21-Z-B", "SF-21-X-D",
        "SF-22-V-C", "SF-22-Y-A", "SF-22-Y-C", "SF-22-V-D",
        "SF-22-V-B", "SF-22-Y-B", "SF-22-Y-D", "SF-22-X-C",
        "SF-22-Z-A", "SF-22-Z-C", "SF-22-X-A", "SE-22-Z-C",
        "SE-22-Z-A", "SE-22-Y-D", "SE-22-Z-B", "SE-22-Z-D",
        "SF-22-X-B", "SE-23-Y-C", "SF-23-V-A", "SF-23-V-C",
        "SF-23-Y-A", "SF-22-X-D", "SF-22-Z-B", "SF-22-Z-D",
        "SG-22-X-A", "SG-22-X-B", "SG-22-X-C", "SG-22-X-D",
        "SF-23-Y-C", "SG-23-V-A", "SG-23-V-C", "SG-22-Z-B",
        "SG-22-Z-D", "SG-22-Z-A", "SG-22-Z-C", "SH-22-X-A",
        "SG-22-Y-D", "SG-22-Y-B", "SH-22-V-B", "SH-22-V-A",
        "SG-22-Y-C", "SG-22-Y-A", "SG-22-V-D", "SG-22-V-B",
        "SG-22-V-A", "SG-22-V-C", "SH-22-V-C", "SH-22-X-C",
        "SH-22-V-D", "SH-22-X-B", "SH-22-X-D"
    ],
    "PANTANAL": [
        "SE-21-X-B", "SE-21-X-D", "SE-21-Z-B", "SE-21-Z-C",
        "SE-21-Z-A", "SE-21-X-C", "SE-21-X-A", "SE-21-Y-B",
        "SE-21-V-D", "SE-21-V-B", "SE-21-Y-D", "SE-21-V-A",
        "SD-21-Y-C", "SD-21-Y-D", "SD-21-Z-C", "SF-21-Y-B",
        "SF-21-V-D", "SF-21-V-B", "SF-21-X-A", "SE-21-Z-D"
    ],
    "PAMPA": [
        "SH-21-Y-B", "SH-21-V-D", "SH-21-X-A", "SH-21-X-C",
        "SH-21-X-D", "SH-21-X-B", "SG-21-Z-D", "SG-22-Y-D",
        "SH-22-V-B", "SH-22-V-A", "SG-22-Y-C", "SH-22-V-C",
        "SH-21-Z-B", "SH-22-Y-A", "SH-21-Z-D", "SH-22-Y-C",
        "SI-22-V-A", "SI-22-V-C", "SH-22-Y-D", "SH-22-Y-B",
        "SI-22-V-B", "SH-22-Z-C", "SH-22-Z-A", "SH-22-X-C",
        "SH-22-V-D", "SH-21-Z-C", "SH-21-Z-A"
    ]
}

collectionIds = {
    's2_toa': 'COPERNICUS/S2',
    's2': 'COPERNICUS/S2_SR',
    's2_harmonized': 'COPERNICUS/S2_HARMONIZED',
}

sentinelIds = {
    's2_toa': 'sentinel-2 (toa)',
    's2_harmonized': 'sentinel-2 (harmonized)',
}

outputCollections = {
    's2_harmonized': 'projects/nexgenmap/MapBiomas2/SENTINEL/mosaics-3',
}

bufferSize = 100

yearsSat = [
    # [2016, 's2_harmonized'],
    # [2017, 's2_harmonized'],
    # [2018, 's2_harmonized'],
    # [2019, 's2_harmonized'],
    # [2020, 's2_harmonized'],
    # [2021, 's2_harmonized'],
    # [2022, 's2_harmonized'],
    [2023, 's2_harmonized'],
]

S2_CLOUD_PROBABILITY = 'COPERNICUS/S2_CLOUD_PROBABILITY'


def multiplyBy10000(image):

    bands = [
        'blue',
        'green',
        'red_edge_1',
        'red_edge_2',
        'red_edge_3',
        'red',
        'red_edge_4',
        'nir',
        'swir1',
        'swir2',
        'cai',
        'evi2',
        'gcvi',
        'hallcover',
        'hallheigth',
        'ndvi',
        'ndwi',
        'pri',
        'savi',
    ]

    return image.addBands(
        srcImg=image.select(bands).multiply(10000),
        names=bands,
        overwrite=True
    )


def divideBy10000(image):

    bands = [
        'blue',
        'green',
        'red_edge_1',
        'red_edge_2',
        'red_edge_3',
        'red',
        'red_edge_4',
        'nir',
        'swir1',
        'swir2',
    ]

    return image.addBands(
        srcImg=image.select(bands).divide(10000),
        names=bands,
        overwrite=True
    )


def maskEdges(primary, secondary, leftField, rightField):
    """
    """
    joined = ee.Join.saveFirst('orbit')\
        .apply(primary=primary,
               secondary=secondary,
               condition=ee.Filter.equals(
                   leftField=leftField,
                   rightField=rightField
        )
    )
    
    joined = ee.ImageCollection(joined)
    
    joined = joined.map(
        lambda image: ee.Image(image).multiply(
            ee.Image(ee.Image(image).get('orbit')))
                .copyProperties(image)
                .copyProperties(image, ['system:time_start'])
    )

    return ee.ImageCollection(joined)


def applyCloudMask(collection, dateStart, dateEnd, geometry, maxCloudProbability=40):

    def _getCloudMask(image):

        clouds = image.select(['probability'])

        cloudMask = clouds.gt(maxCloudProbability)\
            .rename(['cloudMask'])

        return image.addBands(cloudMask)

    def _getShadowMask(image):

        image = cloudProject(image,
                             shadowSumThresh=6000,
                             dilatePixels=2,
                             cloudHeights=[
                                 200, 700, 1200, 1700, 2200, 2700,
                                 3200, 3700, 4200, 4700
                             ],
                             cloudBand='cloudMask')

        return image

    criteria = ee.Filter.date(dateStart, dateEnd)

    cloudProbability = ee.ImageCollection(S2_CLOUD_PROBABILITY)\
        .filter(criteria)\
        .filterBounds(grid)

    collectionWithCloudMask = ee.ImageCollection(collection.combine(cloudProbability))\
        .map(_getCloudMask)

    collectionWithCloudMask = tdom(collectionWithCloudMask,
                                   zScoreThresh=-1,
                                   shadowSumThresh=6000,
                                   dilatePixels=2)

    collectionWithCloudMask = collectionWithCloudMask.map(_getShadowMask)

    collectionWithoutClouds = collectionWithCloudMask \
        .map(
            lambda image: image.mask(
                image.select([
                    'cloudMask',
                    'cloudShadowTdomMask'
                ]).reduce(ee.Reducer.anyNonZero()).eq(0)
            )
        )

    return collectionWithoutClouds


orbits = ee.ImageCollection(ASSET_ORBITS)\
    .map(lambda image: image.set('orbit', ee.Number.parse(image.get('orbit'))))

for year, satellite in yearsSat:

    for biomeName in biomeNames:

        grids = ee.FeatureCollection(ASSET_GRIDS)\
            .filter(
            ee.Filter.inList('grid_name', gridNames[biomeName])
        )

        dateStart = '{}-{}'.format(year, dataFilter[biomeName]['dateStart'])
        dateEnd = '{}-{}'.format(year, dataFilter[biomeName]['dateEnd'])
        cloudCover = dataFilter[biomeName]['cloudCover']
        
        for gridName in gridNames[biomeName]:

            try:
                # if True:
                alreadyInCollection = ee.ImageCollection(outputCollections[satellite]) \
                    .filterMetadata('year', 'equals', year) \
                    .filterMetadata('biome', 'equals', biomeName) \
                    .reduceColumns(ee.Reducer.toList(), ['system:index']) \
                    .get('list') \
                    .getInfo()

                outputName = biomeName + '-' + \
                    gridName + '-' + \
                    str(year) + '-' + \
                    str(version[biomeName])

                if outputName not in alreadyInCollection:
                    # define a geometry
                    grid = grids.filter(ee.Filter.stringContains(
                        'grid_name', gridName))

                    grid = ee.Feature(grid.first()).geometry()\
                        .buffer(bufferSize).bounds()

                    # returns a collection containing the specified parameters
                    collection = getCollection(collectionIds[satellite],
                                               dateStart=str(year) + '-01-01',
                                               dateEnd=str(year) + '-12-30',
                                               cloudCover=70,
                                               geometry=grid,
                                               scaleFactor=False
                                               )

                    # returns a pattern of band names
                    bands = getBandNames(satellite)

                    # Rename collection image bands
                    collection = collection.select(
                        bands['bandNames'],
                        bands['newNames']
                    )

                    endmember = ENDMEMBERS[sentinelIds[satellite]]

                    collection = applyCloudMask(collection,
                                                dateStart=dateStart,
                                                dateEnd=dateEnd,
                                                geometry=grid,
                                                maxCloudProbability=CLOUD_PROBABILITY[biomeName])

                    collection = collection.map(
                        lambda image: getFractions(image, endmember))
                    
                    # calculate SMA indexes
                    collection = collection\
                        .map(getNDFI)\
                        .map(getSEFI)\
                        .map(getWEFI)\
                        .map(getFNS)

                    # calculate Spectral indexes
                    collection = collection\
                        .map(divideBy10000)\
                        .map(getCAI)\
                        .map(getEVI2)\
                        .map(getGCVI)\
                        .map(getHallCover)\
                        .map(getHallHeigth)\
                        .map(getNDVI)\
                        .map(getNDWI)\
                        .map(getPRI)\
                        .map(getSAVI)\
                        .map(multiplyBy10000)
                    
                    # remove noised edges
                    collection = maskEdges(
                        primary=collection,
                        secondary=orbits,
                        leftField='SENSING_ORBIT_NUMBER',
                        rightField='orbit'
                    )

                    # generate mosaic
                    if biomeName in ['PANTANAL']:
                        percentileBand = 'ndwi'
                    else:
                        percentileBand = 'ndvi'

                    mosaic = getMosaic(collection,
                                       percentileDry=25,
                                       percentileWet=75,
                                       percentileBand=percentileBand,
                                       dateStart=dateStart,
                                       dateEnd=dateEnd)

                    mosaic = getSlope(mosaic)
                    mosaic = getEntropyG(mosaic)
                    mosaic = setBandTypes(mosaic, mtype="biomes_s2")

                    mosaic = mosaic.set('year', year)
                    mosaic = mosaic.set('collection', 7.0)
                    mosaic = mosaic.set('grid_name', gridName)
                    mosaic = mosaic.set('version', str(version[biomeName]))
                    mosaic = mosaic.set('biome', biomeName)
                    mosaic = mosaic.set('satellite', satellite)

                    print(outputName)

                    task = ee.batch.Export.image.toAsset(
                        image=mosaic,
                        description=outputName,
                        assetId=outputCollections[satellite] +
                        '/' + outputName,
                        region=grid.coordinates().getInfo(),
                        scale=10,
                        maxPixels=int(1e13)
                    )

                    task.start()

            except Exception as e:
                print(e)
