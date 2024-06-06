from .vpic_info import *
from .kfilter import *
from .pderiv import *
from .load_vars import* 
import numpy as np
import pandas as pd

def QD_calc(dirs, t, sp = 'electron'):
  times = get_times(dirs)
  vpic_info = get_vpic_info(dirs)
  el = load_hydro_fil(dirs, times[t], sp)

  dx = vpic_info['dx/de']
  dy = vpic_info['dy/de']

  uxe = el['jx']/el['rho']
  uye = el['jy']/el['rho']
  uze = el['jz']/el['rho']

  dux_dx = pderiv(uxe,dx=dx,ax=0,order=2,smth=None)
  duy_dx = pderiv(uye,dx=dx,ax=0,order=2,smth=None)
  duz_dx = pderiv(uze,dx=dx,ax=0,order=2,smth=None)
  dux_dy = pderiv(uxe,dx=dy,ax=1,order=2,smth=None)
  duy_dy = pderiv(uye,dx=dy,ax=1,order=2,smth=None)
  duz_dy = pderiv(uze,dx=dy,ax=1,order=2,smth=None)   

  theta = np.array(dux_dx + duy_dy)

  Dxx = np.array(dux_dx) - (1/3)*theta 

  Dyy = np.array(duy_dy) - (1/3)*theta
  Dzz = 0 - (1/3)*theta

  Dxy = np.array((1/2)*(dux_dy + duy_dx))
  Dxz = np.array((1/2)*(duz_dx))
  Dyz = np.array((1/2)*(duz_dy))

  QD_nrm = (Dxx*Dxx+Dyy*Dyy+Dzz*Dzz+ 2.* np.array(Dxy*Dxy+Dxz*Dxz+Dyz*Dyz))

  QD = (1/2) * QD_nrm/(2 * np.average(QD_nrm))
  return QD

def QJ_calc(dirs, t):
  times = get_times(dirs)
  vpic_info = get_vpic_info(dirs)
  dx = vpic_info['dx/de']
  dy = vpic_info['dy/de']

  el = load_hydro_fil(dirs, times[t], 'electron')
  ion = load_hydro_fil(dirs, times[t], 'ion')

  je2 = (el['jx'] + el['jy'] + el['jz'])**2
  ji2 = (ion['jx'] + ion['jy'] + ion['jz'])**2
  j2 = (el['jx'] + ion['jx'] + el['jy']+ ion['jy'] + el['jz'] + ion['jz'])**2
  QJe = (1/4) * je2/np.average(je2)
  QJi = (1/4) * ji2/np.average(ji2)
  QJ = (1/4) * je2/np.average(je2)

  return QJe, QJi, QJ
