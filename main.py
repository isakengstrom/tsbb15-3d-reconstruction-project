import scipy
from scipy import linalg
import scipy.cluster
import numpy as np
import fun
import cv2 as cv
import scipy.io as sio
print("Hello World")


img1 = cv.imread("images/viff.000.ppm", cv.IMREAD_COLOR)
img2 = cv.imread("images/viff.001.ppm", cv.IMREAD_COLOR)
img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

F, *_ = fun.f_matrix(img1, img2)

Dino_36C = sio.loadmat('imgdata\dino_Ps.mat')

Dino_36C = Dino_36C['P']
#print(Dino_36C)
C = np.asarray(Dino_36C.tolist())
K = np.zeros((C.shape[1],3,3))
R = np.zeros((C.shape[1],3,3))
t = np.zeros((C.shape[1],3))

for i in range(C.shape[1]):
    K[i,:,:], R[i,:,:], t[i,:] = fun.camera_resectioning(C[0,i,:,:])

#E = K.T*F*K
E = np.matmul(np.transpose(K),np.matmul(F,K))
#print(K)
#The second camera. This is always [I | 0]
C1, C2 = lab3.fmatrix_cameras(E)
M = np.ones((3,3))
U, S, V = fun.specSVD(M)

R, t = fun.relative_camera_pose(E, C1, C2, d)
print(R)
print(t)
