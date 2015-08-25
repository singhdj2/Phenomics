__author__ = 'singhdj2'

#GDAL based program to access the image and Geotiff exif information.
#only works for some JPEGs and Tiffs
from osgeo import gdal
gjpeg = gdal.Open( "/Users/singhdj2/Desktop/IMG_4887.JPG" )

meta_dict = gjpeg.GetMetadata()

#print type(meta_dict)
#print dir(meta_dict)

for tag, value in meta_dict.items():
    print tag, ':', value



