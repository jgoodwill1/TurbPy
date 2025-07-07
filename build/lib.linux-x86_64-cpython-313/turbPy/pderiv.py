from scipy.ndimage import gaussian_filter as gf
import numpy as np

def pderiv(ar,dx=1.,ax=0,order=2,smth=None):
   """
      pderiv gives the first partial derivative
      of a periodic array along a given axis.

      Inputs:
         ar - The input array
         dx - Grid spacing, defaults to 1.
         ax - Axis along which to take the derivative
         order - Order of accuracy, (1,2) defaults to 2

      Output:
         dar - The derivative array
   """
   ar = np.array(ar)
   if smth is not None:
      ar = gf(ar,sigma=smth)
   if order == 1:
      dar = (np.roll(ar,-1,axis=ax)-ar)/dx
   elif order == 2:
      dar = (np.roll(ar,-1,axis=ax)-np.roll(ar,1,axis=ax))/(2*dx)
   
   return dar 

def pcurl(arx,ary,arz,dx=1,dy=1,dz=1,smth=None):
   return pderiv(arz,dx=dy,ax=1,smth=smth),\
          pderiv(arz,dx=dx,ax=0,smth=smth),\
          pderiv(ary,dx=dx,ax=0,smth=smth)-pderiv(arx,dx=dy,ax=1,smth=smth)