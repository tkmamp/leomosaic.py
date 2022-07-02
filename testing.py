from src.imaging import BasicImage, MosaicTile, Mosaic
from PIL import Image
from os import listdir
from os.path import isfile, join


mymosaic = Mosaic()
#target_im = "/data_partition/Sciebo/Bilder/Roadtrip21/20210705_181727.jpg"
#source_dir = "/data_partition/Sciebo/Bilder/Roadtrip21/"
target_im = "data/testset/2-format2020.jpg"
source_dir = "data/testset/"
w = 4000
h = int(w*9/16)
mymosaic.create_image_mosaic(target_im, source_dir, target_resolution_wh=(w, h), target_number_tiles_wh=(5, 5), overlay=0.5)
mymosaic.blended_mosaic.show()
