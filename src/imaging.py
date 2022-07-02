import matplotlib.pyplot as plt


class BasicImage():
    def __init__(self, im=None) -> None:
        self.im = im
        if im is not None:
            self.set_res(im)
        else:
            self.res_wh = None

    def set_im(self, im):
        self.im = im
        self.set_res(im)

    def set_res(self, im):
        self.res_wh = [im.shape[1], im.shape[0]]

    def get_im(self):
        return self.im

    def show_im(self):
        if self.im is not None:
            plt.imshow(self.im)
            plt.show()
        else:
            print("no image")
 

class MosaicTile(BasicImage):
    def __init__(self, im=None) -> None:
        super().__init__(im)

    def set_im(self, im):
        # resize to tile-size
        # save as self.im
        pass

    def set_tile_mean_color(self):
        # calc mean color of tile for mosaic construction
        pass

    def resize_im(self, im):
        pass


class Mosaic(BasicImage):
    def __init__(self) -> None:
        super().__init__(im=None)
        self.source_dir = None
        self.tiles = []
        self.tiles_mean_colors = None
        self.mosaic = None
        self.res_mosaic = None
        self.res_tiles_wh = None
    
    def set_mosaic_res(self, res):
        self.res_mosaic = res

    def set_tiles(self):
        pass

    def set_res_tiles(self):
        pass

    def set_tiles_mean_colors(self):
        pass

    def set_mosaic(self):
        pass

    def get_target_mean_colors(self):
        pass

    def overlay_mosaic(self, intensity):
        pass

    def create_image_mosaic(self, target_image, target_resolution_wh, tile_source_dir, target_resolution_tiles_wh=[], overlay=0.)
        pass
    

    
    


