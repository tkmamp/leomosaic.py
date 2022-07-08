from src.imaging import Mosaic


mymosaic = Mosaic()
target_im = "data/geschenk_leo/main.jpg" # load pics into that folder
source_dir = "data/geschenk_leo/tiles/" # target image
w = 14043  # 14043x9933 ist lt. internet die Auflösung für DIN A0, 300 dpi
h = 9933 # int(w*3/4)
w_tiles = 60 
h_tiles = w_tiles #int(w_tiles*3/4)
mymosaic.create_image_mosaic(target_im, source_dir, reuse_images=False, max_reuse=100, 
                             target_resolution_wh=(w, h), target_number_tiles_wh=(w_tiles, h_tiles), 
                             overlay=0.4, kshape=(5,5), desaturate=0.8)
mymosaic.blended_mosaic.save(fp="C:\\Users\\Tobia\\Desktop\\demo.png") # save to this file
print("ready")