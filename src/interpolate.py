from .load_vars import *
import numpy as np

def B_interpolate(dirs, time):
  ds = load_vars(dirs, time)
  Bx = (1/2) * (ds['cbx'] + np.roll(ds['cbx'], 1, axis = 0)) 
  By = (1/2) * (ds['cby'] + np.roll(ds['cby'], 1, axis = 1))
  return Bx, By

def E_interpolate(dirs, time):
  ds = load_vars(dirs, time)
  ExF = (1/2) * (ds['ex'] + np.roll(ds['ex'], 1, axis = 1)) 
  EyF = (1/2) * (ds['ey'] + np.roll(ds['ey'], 1, axis = 0))
 
  Ex = (1/2) * (ExF + np.roll(ExF, 1, axis = 0)) 
  Ey = (1/2) * (EyF + np.roll(EyF, 1, axis = 1))
  return Ex, Ey