from src.imaging import BasicImage, MosaicTile, Mosaic
from PIL import Image
from os import listdir
from os.path import isfile, join

im = Image.open("data/testset/iStock-667024182.webp")

mytile = MosaicTile("data/testset/iStock-667024182.webp", (1000, 400))

onlyfiles = [f for f in listdir("data/testset/") if isfile(join("data/testset/", f))]


mymosaic = Mosaic()
target_im = "data/testset/meme--1-.jpg"
mymosaic.create_image_mosaic(target_im, (1000, 1000), "data/testset/", (20, 20), 0.6)
mymosaic.blended_mosaic.show()
