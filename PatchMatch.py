import random
import numpy as np
import math
import Image

Img_A = "bike_a.png"
Img_B = "bike_b.png"

boxsize = 7


class nnf:
    
    def __init__(self, Img_A, Img_B, boxsize):
        self.Img_A = Image.open(Img_A)
        self.Img_B = Image.open(Img_B)
        self.boxsize = boxsize   
        
    # calculate offset in terms of sum of square differences
    def cal_offset(self, ax, ay, bx, by):       
        box_A = (ax, ay, ax+self.boxsize, ay+self.boxsize)
        box_B = (bx, by, bx+self.boxsize, by+self.boxsize)
        self.patch_A = self.Img_A.crop(box_A)
        self.patch_B = self.Img_B.crop(box_B)
        self.abs_diff = np.array(self.patch_A) - np.array(self.patch_B)
        self.ssd = math.sqrt(np.sum([x*x for x in self.abs_diff]))
        return self.ssd
        
   # nearest-neighbor-field random initialization, return correspondences in three channels: x_coordinates, y_coordinates, offsets
    def init_nnf(self):
        bxs = [random.randint(0, self.Img_B.size[1] - self.boxsize) for i in range((self.Img_B.size[0]- self.boxsize)*(self.Img_B.size[1]- self.boxsize)) ]
        bys = [random.randint(0, self.Img_B.size[0] - self.boxsize) for i in range((self.Img_B.size[0]- self.boxsize)*(self.Img_B.size[1]- self.boxsize)) ]
        self.nnf_x = np.zeros((self.Img_A.size[0]- self.boxsize, self.Img_A.size[1]- self.boxsize))
        self.nnf_y = np.zeros((self.Img_A.size[0]- self.boxsize, self.Img_A.size[1]- self.boxsize))
        self.nnf_D = np.zeros((self.Img_A.size[0]- self.boxsize, self.Img_A.size[1]- self.boxsize))
        k=0
        for i in range(len(self.nnf_x)):
            for j in range(len(self.nnf_x[0])):
                self.nnf_x[i][j] = bxs[k]
                self.nnf_x[i][j] = bys[k]
                self.nnf_D[i][j] = self.cal_offset(i, j, bxs[k], bys[k])
                k = k + 1
        return self.nnf_x, self.nnf_y, self.nnf_D
    
    # improve nnf offsets by searching and comparing neighbor's offsets
    def improve_nnf:
                
        


