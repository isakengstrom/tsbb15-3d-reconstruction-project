import lab3
import cv2 as cv
import numpy as np
import scipy
from matplotlib import pyplot as plt
from scipy.optimize import least_squares
import math

def matchingMatrix(roi1, roi2) :
    matrix = np.empty((len(roi1),len(roi2)))
    # the matching score is the MSE
    for i in range(len(roi1)) :
        for j in range(len(roi2)) :
            matrix[i,j] = np.linalg.norm(roi1[i] - roi2[j])
            #print(matrix[i,j])
    return matrix

def f_matrix(img1, img2) :

    point = np.loadtxt('imgdata\points.txt')
    points = point[:,:4]
    coords1_t = points[:,0:2]
    coords2_t = points[:,2:4]
    coords1_t = coords1_t[np.any(coords1_t != -1, axis=1), :]
    coords2_t = coords2_t[np.any(coords2_t != -1, axis=1), :]
    coords2_t = coords2_t[:coords1_t.shape[0],:]
    coords1 = coords1_t.T
    coords2 = coords2_t.T
    # plt.imshow(img1)
    # plt.scatter(coords1[0], coords1[1])
    # plt.show()

    F, mask = cv.findFundamentalMat(coords1_t, coords2_t, cv.FM_RANSAC)

    # We select only inlier points
    coords1_t = coords1_t[mask.ravel()==1]
    coords2_t = coords2_t[mask.ravel()==1]

    inl_coords1 = coords1_t.T
    inl_coords2 = coords2_t.T

    lab3.show_corresp(img1, img2, inl_coords1, inl_coords2)
    plt.show()

    # camera 1 and 2
    C1, C2 = lab3.fmatrix_cameras(F)
    X = np.empty((3,inl_coords1.shape[1]))
    for i in range(inl_coords1.shape[1]) :
        X[:,i] = lab3.triangulate_optimal(C1, C2, inl_coords1[:,i], inl_coords2[:,i])

    # minimize using least_squares
    params = np.hstack((C1.ravel(), X.T.ravel()))
    solution = least_squares(lab3.fmatrix_residuals_gs, params, args=(inl_coords1,inl_coords2))
    print("snabbt")
    C1 = solution.x[:12].reshape(3,4)
    F_gold = lab3.fmatrix_from_cameras(C1, C2)

    return F_gold, inl_coords1, inl_coords2

#input 3 x 4 camera matrix
def camera_resectioning(C):
    A = C[:,0:3]
    b = C[:,3]

    U, Q = specRQ(A)
    t = np.matmul(np.matrix.transpose(U), b)
    U = U/U[2,2]
    D = np.sign(U)
    K = U*D

    if np.linalg.det(D) == 1:
        R = np.matmul(D,Q)
        t = np.matmul(D,t)
    else:
        R = np.matmul(-1*D,Q)
        t = np.matmul(-1*D,t)
    return K,R,t
