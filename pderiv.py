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