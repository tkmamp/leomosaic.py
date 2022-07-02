from turtle import color
from xml.etree.ElementPath import find
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join



def calc_keypoints(im, m, n):
        keypoints = np.zeros((m, n, 3))
        h_px = int(im.height/m)
        w_px = int(im.width/n)
        w = 0
        for i in range(n):
            h = 0
            for j in range(m):
                for k in range(3):
                    keypoints[j, i, k] = np.mean(im.__array__()[h:h+h_px, w:w+w_px, k])
                h += h_px
            w += w_px
        return keypoints




class BasicImage():
    def __init__(self, source=None) -> None:
        self.source = source
        if source is not None:
            self.load_file(source)
        else:
            self.im = None
            self.res_wh = None

    def load_file(self, source):
        self.source = source
        try:
            self.set_im(Image.open(source))
        except:
            self.set_im(None)
            print(str("could not open " + source))

    def set_im(self, im):
        self.im = im        

    def get_im(self):
        return self.im

    def show_im(self):
        if self.im is not None:
            self.im.show()
        else:
            print("no image")
 

class MosaicTile(BasicImage):
    def __init__(self, source, target_res=None) -> None:
        super().__init__(source)
        self.set_tile_mean_color()
        if target_res is not None:
            self.resize_im(target_res)
        self.set_tile_color_keypoints()

    def set_tile_mean_color(self):
        self.mean_color = [np.mean(self.im.__array__()[:, :, i]) for i in range(3)]

    def set_tile_color_keypoints(self):
        self.mean_keypoints = calc_keypoints(self.im, 3, 3)

    def resize_im(self, target_res):
        self.im = self.im.resize(target_res)
        pass
        

class Mosaic(BasicImage):
    def __init__(self) -> None:
        super().__init__(None)
        self.source_dir = None
        self.tiles = []
        self.tiles_mean_colors = None
        self.target_mean_colors = None
        self.mosaic = None
        self.res_mosaic = None
        self.n_tiles_wh = None
    
    def set_mosaic_res(self, res):
        if res == ():
            res = (self.im.width, self.im.height)
        self.res_mosaic = res
        self.im = self.im.resize(res)

    def set_source_dir(self, source_dir):
        self.source_dir = source_dir

    def set_tiles(self):
        res_tiles = self.get_res_tiles()
        tiles = []
        tiles_mean_colors = []
        tiles_mean_keypoints = []
        files = [f for f in listdir(self.source_dir) if isfile(join(self.source_dir, f))]
        if not self.reuse_images:
            assert(len(files)>=self.n_tiles_wh[0]*self.n_tiles_wh[1]), ''' not enough pictures!!11!!1 '''
        for f in files:
            t = MosaicTile(join(self.source_dir, f), res_tiles)
            tiles.append(t)
            tiles_mean_colors.append(np.array(t.mean_color))
            tiles_mean_keypoints.append(t.mean_keypoints)
        self.tiles = tiles
        self.tiles_mean_colors = tiles_mean_colors
        self.tiles_mean_keypoints = tiles_mean_keypoints

    def set_n_tiles_wh(self, n_tiles_wh):
        self.n_tiles_wh =n_tiles_wh

    def get_res_tiles(self):
        w_tiles = np.floor(self.res_mosaic[0]/self.n_tiles_wh[0])
        h_tiles = np.floor(self.res_mosaic[1]/self.n_tiles_wh[1])
        self.res_mosaic = (int(w_tiles*self.n_tiles_wh[0]), int(h_tiles*self.n_tiles_wh[1]))
        return (int(w_tiles), int(h_tiles))

    def set_target_mean_colors(self):
        target_mean_colors = np.zeros((self.n_tiles_wh[1],  self.n_tiles_wh[0], 3))
        target_keypoints = np.zeros((3, 3, self.n_tiles_wh[1],  self.n_tiles_wh[0], 3))
        w_px, h_px = self.get_res_tiles()
        n = 0
        im = self.im.__array__()
        for i in range(target_mean_colors.shape[0]):
            m = 0
            for j in range(target_mean_colors.shape[1]):
                for k in range(3):
                    target_mean_colors[i, j, k] = np.mean(im[n:n+h_px, m:m+w_px, k])
                target_keypoints[:, :, i ,j, :] = calc_keypoints(Image.fromarray(im[n:n+h_px, m:m+w_px, :]), 3, 3)
                m += w_px
            n += h_px
        self.target_mean_colors = target_mean_colors
        self.target_keypoints = target_keypoints

    def color_dist(self, rgb1, rgb2):
        return np.linalg.norm(rgb1-rgb2)

    def calc_color_dists(self, target_points, tiles_points, keypoints):
        if keypoints:
            return np.array([self.color_dist(target_points, tiles_points[i]) for i in range(len(tiles_points))])
        else:
            return np.array([self.color_dist(target_points, tiles_points[i]) for i in range(len(tiles_points))])

    def get_min_color_dist_idx(self, target_points, tiles_points, keypoints):
        return  np.argmin(self.calc_color_dists(target_points, tiles_points, keypoints))

    def set_mosaic(self, keypoints=True):
        mosaic = np.zeros((self.res_mosaic[1], self.res_mosaic[0], 3))
        w_px, h_px = self.get_res_tiles()
        n = 0
        if keypoints:
            tiles_points = self.tiles_mean_keypoints.copy()
        else:
            tiles_points = self.tiles_mean_colors.copy()
        tiles = self.tiles.copy()

        for i in range(self.n_tiles_wh[1]):
            m = 0
            for j in range(self.n_tiles_wh[0]):
                if keypoints:
                    f_idx = self.get_min_color_dist_idx(self.target_keypoints[:, :, i, j, :], tiles_points, keypoints)
                else:
                    f_idx = self.get_min_color_dist_idx(self.target_mean_colors[i, j, :], tiles_points, keypoints)
                mosaic[n:n+h_px, m:m+w_px, :] = tiles[f_idx].im.__array__()
                m+=w_px
                if not self.reuse_images:
                    tiles_points.pop(f_idx)
                    tiles.pop(f_idx)
            n += h_px
        self.mosaic = Image.fromarray(mosaic.astype(np.uint8))

    def overlay_mosaic(self, alpha):
        self.blended_mosaic = Image.blend(self.mosaic, self.im.resize(self.res_mosaic), alpha)

    def create_image_mosaic(self, target_image, tile_source_dir, reuse_images=False, target_resolution_wh=(), target_number_tiles_wh=(), overlay=0.):
        self.reuse_images = reuse_images        
        self.load_file(target_image)
        self.set_mosaic_res(target_resolution_wh)
        self.set_source_dir(tile_source_dir)
        self.set_n_tiles_wh(target_number_tiles_wh)
        self.set_tiles()
        self.set_target_mean_colors()
        self.set_mosaic()
        self.overlay_mosaic(overlay)
        
        
    

    
    


