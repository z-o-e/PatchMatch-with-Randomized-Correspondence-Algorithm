#! /usr/bin/env python
import random
import numpy as np
import math
import Image
import matplotlib.pyplot as plt

Img_A = "bike_a.png"
Img_B = "bike_b.png"

boxsize = 20

iterations = 3

class nnf:
    
    def __init__(self, Img_A, Img_B, boxsize, iterations):
        self.Img_A = Image.open(Img_A)
        self.Img_B = Image.open(Img_B)
        self.boxsize = boxsize 
        #return correspondences in three channels: x_coordinates, y_coordinates, offsets  
        self.nnf_x = np.zeros((self.Img_A.size[1], self.Img_A.size[0]))
        self.nnf_y = np.zeros((self.Img_A.size[1], self.Img_A.size[0]))
        self.nnf_D = np.zeros((self.Img_A.size[1], self.Img_A.size[0]))

    # calculate offset in terms of sum of square differences
    def cal_offset(self, ax, ay, bx, by):
        # patches out of the boundaries are set to high offset/inifinity
        if bx > self.Img_B.size[0]- self.boxsize or by > self.Img_B.size[1]- self.boxsize:
            self.ssd = 1000
        else:  
            box_A = (ax, ay, ax+self.boxsize, ay+self.boxsize)
            box_B = (bx, by, bx+self.boxsize, by+self.boxsize)
            self.patch_A = self.Img_A.crop(box_A)
            self.patch_B = self.Img_B.crop(box_B)
            self.abs_diff = np.array(self.patch_A) - np.array(self.patch_B)
            self.ssd = math.sqrt(np.sum([x*x for x in self.abs_diff]))
        return self.ssd        

   # nearest-neighbor-field random initialization, return correspondences in three channels: x_coordinates, y_coordinates, offsets
    def init_nnf(self):
        # set up random coordinates 
        b = [ [i,j] for i in range(self.Img_B.size[1]) for j in range(self.Img_B.size[0]) ]
        b = random.sample(b, len(b))
        bys = [b[i][0] for i in range(len(b))]
        print "bymax",max(bys)
        bxs = [b[i][1] for i in range(len(b))]
        print "bxmax",max(bxs)
        k=0
        for y in range(self.Img_A.size[1]):
            for x in range(self.Img_A.size[0]):
                self.nnf_x[y][x] = bxs[k]
                self.nnf_y[y][x] = bys[k]
                self.nnf_D[y][x] = self.cal_offset(i, j, bxs[k], bys[k])
                k = k + 1
        return self.nnf_x, self.nnf_y, self.nnf_D 
           
    # improve nnf offsets by searching and comparing neighbor's offsets
    def improve_nnf(self):
        print "y",self.Img_A.size[1]
        print "x",self.Img_A.size[0]
        for r in range(iterations):
            for y in range(self.Img_A.size[1]):
                for x in range(self.Img_A.size[0]):
                    # find among self and neighbors up-above and left the best match and recalcuate the offset
                    # first row only has left neighbor
                    if y==0 and x!=0:
                        left = self.cal_offset(y, x, int(self.nnf_y[y][x-1]), int(self.nnf_x[y][x-1])+1)
                        m = min(self.nnf_D[y][x], left)
                        if m == left:
                            self.nnf_D[y][x] = left
                            self.nnf_x[y][x] = int(self.nnf_x[y][x-1])+1
                            self.nnf_y[y][x] = int(self.nnf_y[y][x-1])
                    #first column only has up neighbor        
                    if x==0 and y!=0:
                        up = self.cal_offset(y, x, int(self.nnf_y[y-1][x])+1, int(self.nnf_x[y-1][x]))
                        m = min(self.nnf_D[y][x], up)
                        if m == up:
                            self.nnf_D[y][x] = up
                            self.nnf_x[y][x] = int(self.nnf_x[y-1][x])
                            self.nnf_y[y][x] = int(self.nnf_y[y-1][x])+1
                            
                    if y!=0 and x!=0:
                        left =  self.cal_offset(y, x, int(self.nnf_y[y][x-1]), int(self.nnf_x[y][x-1])+1)
                        up = self.cal_offset(y, x, int(self.nnf_y[y-1][x])+1, int(self.nnf_x[y-1][x]))
                        m = min(self.nnf_D[y][x], self.nnf_D[y-1][x], self.nnf_D[y][x-1])
                        print (self.nnf_D[y][x]>m)
                        if m == up:
                            self.nnf_D[y][x] = up
                            self.nnf_x[y][x] = int(self.nnf_x[y-1][x])
                            self.nnf_y[y][x] = int(self.nnf_y[y-1][x])+1                                   
                        if m == left :
                            self.nnf_D[y][x] = left
                            self.nnf_x[y][x] = int(self.nnf_x[y][x-1])+1
                            self.nnf_y[y][x] = int(self.nnf_y[y][x-1])

        return self.nnf_x, self.nnf_y, self.nnf_D
                

test=nnf(Img_A, Img_B, boxsize, iterations)

test.init_nnf()

test.improve_nnf()         









    
        


