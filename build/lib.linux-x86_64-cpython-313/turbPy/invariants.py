from .vpic_info import *
from .kfilter import *
from .pderiv import *
from .load_vars import * 
from .vorticity import *
import numpy as np
import pandas as pd

def QD_calc(dirs, t, sp = 'electron'):
  times = get_times(dirs)
  vpic_info = get_vpic_info(dirs)
  el = load_hydro_fil(dirs, times[t], sp)

  dx = vpic_info['dx/de']
  dy = vpic_info['dy/de']

  uxe = (el['jx']/el['rho'])[100:1180,:]
  uye = (el['jy']/el['rho'])[100:1180,:]
  uze = (el['jz']/el['rho'])[100:1180,:]

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

  D = (Dxx*Dxx+Dyy*Dyy+Dzz*Dzz+ 2.* np.array(Dxy*Dxy+Dxz*Dxz+Dyz*Dyz))
  D = D[1:-1]
  QD = ((1/4) * D/(np.average(D)))
  # QD = (1/2) * QD_nrm[100:1180,:]/(2 * np.average(QD_nrm[100:1180,:]))
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
  j2 = (el['jx'] + ion['jx'])**2 + (el['jy']+ ion['jy'])**2 + (el['jz'] + ion['jz'])**2
  # QJe = (1/4) * je2/np.average(je2)
  # QJi = (1/4) * ji2/np.average(ji2)
  # QJ = (1/4) * j2/np.average(j2)
  QJe = (1/4) * je2[100:1180]/np.average(je2[100:1180])
  QJi = (1/4) * ji2[100:1180]/np.average(ji2[100:1180])
  j2 = j2[101:1179]
  print(np.shape(j2))
  QJ = ((1/4) * j2/np.average(j2))
  return QJe, QJi, QJ

def Qw_calc(dirs, t, sp = 'electron'):
  # times = get_times(dirs)
  w_arr = w_calc(dirs, t, sp = sp)
  w = (np.sqrt(w_arr[0]**2 + w_arr[1]**2 + w_arr[2]**2))
  # w = (np.sqrt(w_arr[0]**2 + w_arr[1]**2 + w_arr[2]**2))
  # Qw = (1/4) * (w**2)/ np.average((w**2))
  w = w[1:-1]
  Qw = ((1/4) * (w**2)/np.average(w**2))
  return Qw
