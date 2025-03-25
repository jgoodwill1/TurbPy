import numpy as np
cimport numpy as cnp
from libc.math cimport sqrt
from scipy.fft import fftn, fftshift, fftfreq

# Define function with Cython typing
def PerpSpectrumCy(cnp.ndarray[cnp.float64_t, ndim=2] ar,
                 double lenx=2*np.pi, double leny=2*np.pi):
    """
    Computes the perpendicular spectrum of a 2D array using FFT.
    Optimized using Cython.
    """
    if ar.size == 0:
        print('No array provided! Exiting!')
        return None, None
    
    # Remove mean from array
    ar = ar - np.mean(ar)
    
    cdef int nx = ar.shape[0]
    cdef int ny = ar.shape[1]
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] kx = fftshift(fftfreq(nx)) * nx * (2 * np.pi / lenx)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ky = fftshift(fftfreq(ny)) * ny * (2 * np.pi / leny)
    
    cdef cnp.ndarray[cnp.complex128_t, ndim=2] far = fftshift(fftn(ar)) / (nx * ny)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] fftea = 0.5 * np.abs(far) ** 2
    
    cdef int nnx, nny
    cdef cnp.ndarray[cnp.float64_t, ndim=1] kkx, kky
    
    nnx = nx; nny = ny
    kkx = kx; kky = ky

    cdef cnp.ndarray[cnp.float64_t, ndim=1] fekp = np.zeros(min(nnx//2, nny//2), dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] kp = np.zeros((nnx, nny), dtype=np.float64)
    
    cdef int x, y, i
    
    # cdef cnp.ndarray[cnp.float64_t, ndim=2] kx_grid = np.meshgrid(kx, ky, indexing="ij")[0]
    # cdef cnp.ndarray[cnp.float64_t, ndim=2] ky_grid = np.meshgrid(kx, ky, indexing="ij")[1]
    # cdef cnp.ndarray[cnp.float64_t, ndim=2] kp = np.sqrt(kx_grid**2 + ky_grid**2)
    for x in range(nnx):
        for y in range(nny):
            kp[x, y] = sqrt(kkx[x]**2 + kky[y]**2)
    
    cdef double dk = abs(kp[1, 0] - kp[0, 0])
    cdef cnp.ndarray[cnp.float64_t, ndim=1] kk = kp[nnx//2, nny//2:].copy()
    
    cdef double sum_value
    for i in range(len(fekp)):
        sum_value = 0.0
        for x in range(nnx):
            for y in range(nny):
                if kp[x, y] >= kp[nx//2, i+ny//2] - dk and kp[x, y] < kp[nx//2, i+ny//2] + dk:
                    sum_value += fftea[x, y]
        fekp[i] = sum_value
    
    return kk, fekp / dk


import numpy as np
import numpy.fft as nf

def PerpSpectrum(ar,sumax=2,lenx=2*np.pi,leny=2*np.pi,lenz=2*np.pi):
   """
      PerpSpectrum(ar,sumax=2,lenx=2*pi,leny=2*pi,lenz=2*pi)
      ar -> Array to compute the spectrum
      sumax -> Axis of magnetic field direction. Right now only x,y,z = 0,1,2
      lenx,leny,lenz -> System size in x,y,z directions to take into
                        account the anisotropy of system if any

      RETURNS:
      kk -> Wavenumber array
      fekp -> Spectrum of the array
   """
   if len(ar) == 0:
      print('No array provided! Exiting!')
      return
   ar=ar-np.mean(ar)
   nx=np.shape(ar)[0];kx=nf.fftshift(nf.fftfreq(nx))*nx*(2*np.pi/lenx)
   ny=np.shape(ar)[1];ky=nf.fftshift(nf.fftfreq(ny))*ny*(2*np.pi/leny)
 
   far = nf.fftshift(nf.fftn(ar))/(nx*ny); fftea=0.5*np.abs(far)**2
   ffteb = fftea
## DEFINE A TEMPORARY XY PLANE
   if sumax==2:
      nnx=nx; nny=ny
      kkx=kx; kky=ky
## DEFINE THE KPERP VALUES AND CORRESPONDING SPECTRUM
   fekp=np.zeros(min(nnx//2,nny//2))
   kp=np.zeros((nnx,nny))
   for x in range(nnx):
      for y in range(nny):
         kp[x,y]=np.sqrt(kkx[x]**2+kky[y]**2)
   if nnx == 1:
      dk=np.abs(kp[0,1]-kp[0,0])
      kk=kp[0,nny//2:]
   elif nny == 1:
      dk=np.abs(kp[1,0]-kp[0,0])
      kk=kp[nnx//2:,0]
   else:
      dk=np.abs(kp[1,0]-kp[0,0])
      kk=kp[nnx//2,nny//2:]

   for i in range(len(fekp)):
      fekp[i]= np.sum(np.ma.MaskedArray(ffteb, ~((kp[nx//2,i+ny//2]-dk < kp) & (kp < kp[nx//2,i+ny//2]+dk))))

   return kk,fekp/dk