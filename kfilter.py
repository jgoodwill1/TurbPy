import numpy.fft as nf
import numpy as np

def kfilter(ar,kf , lx = 2 * np.pi, ly = 2 * np.pi):
   nx=np.shape(ar)[0]; ny=np.shape(ar)[1]
   kx = nf.fftshift(nf.fftfreq(nx))* 2 * np.pi * (nx/lx)
   ky = nf.fftshift(nf.fftfreq(ny))* 2 * np.pi * (ny/ly)
   mg=np.meshgrid(ky,kx)
   km=np.sqrt(mg[0]**2+mg[1]**2)
   far = nf.fftshift(nf.fftn(ar))
   far = (np.sign(km - kf) - 1.)/(-2.)*far
   arf = np.real(nf.ifftn(nf.ifftshift(far)))
   return kx, ky, arf