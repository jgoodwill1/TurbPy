from .vpic_info import *
from .load_vars import *
import numpy as np
import pandas as pd

def JE_calc(dirs, save = True):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)

  dx = vpic_info['dx/de']
  
  
  ds = pd.DataFrame({'JE': [],
                     'Jx': [],
                     'Jy': [],
                     'Jz': [],
                     'Ex': [],
                     'Ey': [],
                     'Ez': []}
                     )
  # J_av = np.zeros(len(times))
  # E_av = np.zeros(len(times))
  # JE_av = np.zeros(len(times))
  # jeE_av = np.zeros(len(times))
  # jiE_av = np.zeros(len(times))
  # E_m = np.zeros(len(times))

  for t in np.arange(0,len(times)):
    sp = 'electron'
    jxe = load_var('jx', dirs, times[t], sp)
    jye = load_var('jy', dirs, times[t], sp)
    jze = load_var('jz', dirs, times[t], sp)

    sp = 'ion'
    jxi = load_var('jx', dirs, times[t], sp)
    jyi = load_var('jy', dirs, times[t], sp)
    jzi = load_var('jz', dirs, times[t], sp)

    jx0 = jxe + jxi
    jy0 = jye + jyi 
    jz0 = jze + jzi

    ex = load_var('ex', dirs, times[t])
    ey = load_var('ey', dirs, times[t])
    ez = load_var('ez', dirs, times[t])

    jeE = (jxe * ex) + (jye * ey) + (jze * ez)
    jiE = (jxi * ex) + (jyi * ey) + (jzi * ez)
    JE  = (jx0 * ex) + (jy0 * ey) + (jz0 * ez)


    row = pd.DataFrame(
          {'JE': [np.mean(JE ,dtype = np.float64) ],
           'Jx': [np.mean(jx0,dtype = np.float64)],
           'Jy': [np.mean(jy0,dtype = np.float64)],
           'Jz': [np.mean(jz0,dtype = np.float64)],
           'Ex': [np.mean(ex ,dtype = np.float64) ],
           'Ey': [np.mean(ey ,dtype = np.float64) ],
           'Ez': [np.mean(ez ,dtype = np.float64) ]})

    ds = pd.concat([ds, row], ignore_index = True)
    # Jx_av[t] = np.average(jx0)
    # Jy_av[t] = np.average(jy0)
    # Jz_av[t] = np.average(jz0)
    # Ex_av[t] = np.average(ex)
    # Ey_av[t] = np.average(ey)
    # Ez_av[t] = np.average(ez)
    # JE_av[t]  = np.average(JE)
    # jeE_av[t] = np.average(jeE)
    # jiE_av[t] = np.average(jiE)
  if save == True:
    # pd.DataFrame({'JE': JE_av, 'Jx': J_av, 'E': E_av}).to_csv(dirs + 'JE_av.csv', sep = ',')
    ds.to_csv(dirs + 'JE_av.csv', sep = ',')
  return ds

def read_JE(dirs):
  ds = pd.read_csv(dirs + 'JE_av.csv', delimiter = ',')
  # JE = ds['JE']
  return ds