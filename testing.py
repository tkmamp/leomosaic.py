import numpy as np
from src.imaging import Mosaic

d = [150, 300, 400, 600]
n = [65]
a = [0.35]
for i in range(len(d)):
    for j in range(len(n)):
        for k in range(len(a)):
            mymosaic = Mosaic()
            target_im = "data/geschenk_leo/main1.jpeg" # load pics into that folder
            source_dir = "data/geschenk_leo/tiles/" # target image
            dpi = d[i]
            w = int(14043*dpi/300)  # 14043x9933 ist lt. internet die Auflösung für DIN A0, 300 dpi
            h = int(w/np.sqrt(2)) #9933 # int(w*3/4)
            w_tiles = n[j] 
            h_tiles = int(4/(3*np.sqrt(2))*w_tiles) #int(w_tiles*3/4)
            alpha = a[k]
            svname = "demo_" + str(w_tiles) + "_" + str(dpi) + "dpi_alpha" + str(alpha)
            print("format tiles: " + str(round(1189/w_tiles,1)) + " x " + str(round(841/h_tiles, 1)) + " mm")
            mymosaic.create_image_mosaic(target_im, source_dir, reuse_images=False, max_reuse=-1, 
                                        target_resolution_wh=(w, h), target_number_tiles_wh=(w_tiles, h_tiles), 
                                        overlay=alpha, kshape=(10,10), desaturate_tiles=.8, enhance_target=1.25)
            mymosaic.blended_mosaic.save(fp="C:\\Users\\HP\\Desktop\\druck\\"+ svname +".png") # save to this file
            print("ready")
