"""
Seam Carving for Content Aware Image Resizing and Object Removal
Usage: python main.py -i image_input.jpg -o image_output.jpg -w 100
Author: Ruixi Lin, Xudong Shen, and TAs of CS5340
Date: 11-29-2019
Version: v0.1

References:
[1] Avidan, S., & Shamir, A. (2007, August). Seam carving for content-aware image resizing. In ACM Transactions on graphics (TOG) (Vol. 26, No. 3, p. 10). ACM.
"""

import argparse
import cv2
import numpy as np

class SeamCarver:
    '''
    Note: This is only a one-dimensional SeamCarver! It only reduces the width.
    '''
    
    def __init__(self, filename, out_height, out_width):
        self.out_height = out_height
        self.out_width = out_width

        # read in image
        self.in_image = cv2.imread(filename).astype(np.float64)
        self.in_height, self.in_width = self.in_image.shape[: 2]

        # keep tracking resulting image
        self.out_image = np.copy(self.in_image)
        # some large number
        self.constant = 10000000

        # start carving
        self.seams_carving()


    def seams_carving(self):
        delta_col = int(self.out_width - self.in_width)

        if delta_col < 0:
            self.seams_remove_col(delta_col * -1)
        else:
            raise ValueError('Currently this SeamCarver only reduces the width.')

    def seams_remove_col(self, num_pixel):
        for dummy in range(num_pixel):
            energy_map = self.calc_energy_map()
            seam_idx = self.viterbi(energy_map)

            self.delete_seam(seam_idx)

    def calc_energy_map(self):
        b, g, r = cv2.split(self.out_image)
        b_energy = np.absolute(cv2.Scharr(b, -1, 1, 0)) + np.absolute(cv2.Scharr(b, -1, 0, 1))
        g_energy = np.absolute(cv2.Scharr(g, -1, 1, 0)) + np.absolute(cv2.Scharr(g, -1, 0, 1))
        r_energy = np.absolute(cv2.Scharr(r, -1, 1, 0)) + np.absolute(cv2.Scharr(r, -1, 0, 1))
        return b_energy + g_energy + r_energy

    def delete_seam(self, seam_idx):
        m, n = self.out_image.shape[: 2]
        output = np.zeros((m, n - 1, 3))
        for row in range(m):
            col = seam_idx[row]
            output[row, :, 0] = np.delete(self.out_image[row, :, 0], [col])
            output[row, :, 1] = np.delete(self.out_image[row, :, 1], [col])
            output[row, :, 2] = np.delete(self.out_image[row, :, 2], [col])
        self.out_image = np.copy(output)

    def save_result(self, filename):
        cv2.imwrite(filename, self.out_image.astype(np.uint8))

    def viterbi(self,energy_map):
        '''
        Arguments:
            energy_map: 111x164 int matrix
        Outputs:
            seam_idx: a list of the column indexes in each row, length is 111
        '''
        
        # initialize size
        tem_height, tem_width = self.out_image.shape[:2]
        
        # initialize variables
        seam_idx = np.zeros(tem_height).astype(int)
        phi = np.zeros([tem_height, tem_width]).astype(int)
        w_old = np.zeros(tem_width)
        w_current = np.zeros(tem_width)
        
        # define some simple functions        
        def p_transition(next_z, z):
            if abs(next_z-z) <= 1:
                return 1
            else:
                return self.constant
        
        # forward passing
        for row in range(tem_height):
            if row == 0:
                w_current = energy_map[row,:]
                w_old = np.copy(w_current)
            else:
                for k in range(tem_width):
                    if k == 0:
                        for i in [0, 1]:
                            if i == 0:
                                Min = p_transition(k,i) + w_old[i]
                                Min_index = i
                            else:
                                B = p_transition(k,i) + w_old[i]
                                if B < Min:
                                    Min = B
                                    Min_index = i
                    elif k == (tem_width - 1):
                        for i in [tem_width - 2, tem_width - 1]:
                            if i == tem_width - 2:
                                Min = p_transition(k,i) + w_old[i]
                                Min_index = i
                            else:
                                B = p_transition(k,i) + w_old[i]
                                if B < Min:
                                    Min = B
                                    Min_index = i
                    else:
                        for i in [k-1, k, k+1]:
                            if i == k-1:
                                Min = p_transition(k,i) + w_old[i]
                                Min_index = i
                            else:
                                B = p_transition(k,i) + w_old[i]
                                if B < Min:
                                    Min = B
                                    Min_index = i
                    w_current[k] = energy_map[row,k] + Min
                    phi[row,k] = Min_index
                    
                w_old = np. copy(w_current)
                    
        # backtracking
        for row in range(tem_height-1, -1, -1):
            if row == tem_height-1:
                for k in range(tem_width):
                    if k == 0:
                        Min = w_current[k]
                        seam_idx[row] = k
                    else:
                        if w_current[k] < Min:
                            Min = w_current[k]
                            seam_idx[row] = k
            else:
                seam_idx[row] = phi[row+1,seam_idx[row+1]]
        return seam_idx
                        

if __name__ == '__main__':
    '''
    Note: This is only a one-dimensional SeamCarver. It only reduces the width.
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help = 'input image name/path')
    parser.add_argument('-o', '--output', help = 'output image name/path')
    parser.add_argument('-w', '--width_out', type=int, help = 'output width')
    args = parser.parse_args()

    height_in, width_in = cv2.imread(args.input).astype(np.float64).shape[: 2]
    print('Original image size: ', height_in, width_in)
    
    if args.width_out >= width_in:
        raise ValueError("output width must be smaller than input width. Currently this SeamCarver only supports reducing weight.")
    
    print('Carving...')
    height_out = height_in
    obj = SeamCarver(args.input, height_out, args.width_out)
    obj.save_result(args.output)







