from .vpic_info import *
from .load_vars import *
import numpy as np
import pandas as pd
import xarray as xar

def JE_calc(dirs, t, filt = True, save = True):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)

  dx = vpic_info['dx/de']
  if filt == False:
    sp = 'electron'
    jxe = load_var('jx', dirs, t, sp)
    jye = load_var('jy', dirs, t, sp)
    jze = load_var('jz', dirs, t, sp)

    sp = 'ion'
    jxi = load_var('jx', dirs, t, sp)
    jyi = load_var('jy', dirs, t, sp)
    jzi = load_var('jz', dirs, t, sp)

    jx0 = jxe + jxi
    jy0 = jye + jyi 
    jz0 = jze + jzi

    ex = load_var('ex', dirs, t)
    ey = load_var('ey', dirs, t)
    ez = load_var('ez', dirs, t)

    jeE = (jxe * ex) + (jye * ey) + (jze * ez)
    jiE = (jxi * ex) + (jyi * ey) + (jzi * ez)
    JE  = (jx0 * ex) + (jy0 * ey) + (jz0 * ez)
  if filt == True:
    el = load_hydro_fil(dirs, t, species = 'electron')
    ion = load_hydro_fil(dirs, t, species = 'ion')
    f = load_field_fil(dirs, t)

    jx0 = el['jx'] + ion['jx']
    jy0 = el['jy'] + ion['jy']
    jz0 = el['jz'] + ion['jz']
    JiE = (ion['jx'] * f['ex']) + (ion['jy'] * f['ey']) + (ion['jz'] * f['ez'])
    JeE = (el['jx'] * f['ex']) + (el['jy'] * f['ey']) + (el['jz'] * f['ez'])
    JE  = (jx0 * f['ex']) + (jy0 * f['ey']) + (jz0 * f['ez'])
  return JiE, JeE, JE

def JE_av(dirs, filt = True, save = True):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)

  dx = vpic_info['dx/de']
  
  
  ds = pd.DataFrame({'JE': [],
                     'JiE': [],
                     'JeE': []}
                     )
  # J_av = np.zeros(len(times))
  # E_av = np.zeros(len(times))
  # JE_av = np.zeros(len(times))
  # jeE_av = np.zeros(len(times))
  # jiE_av = np.zeros(len(times))
  # E_m = np.zeros(len(times))

  for t in np.arange(0,len(times)):
    if filt == False:
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
    if filt == True:
      el = load_hydro_fil(dirs, times[t], species = 'electron')
      ion = load_hydro_fil(dirs, times[t], species = 'ion')
      f = load_field_fil(dirs, times[t])

      jx0 = el['jx'] + ion['jx']
      jy0 = el['jy'] + ion['jy']
      jz0 = el['jz'] + ion['jz']
      JiE = (ion['jx'] * f['ex']) + (ion['jy'] * f['ey']) + (ion['jz'] * f['ez'])
      JeE = (el['jx'] * f['ex']) + (el['jy'] * f['ey']) + (el['jz'] * f['ez'])
      JE  = (jx0 * f['ex']) + (jy0 * f['ey']) + (jz0 * f['ez'])


    row = pd.DataFrame(
          {'JE': [np.mean(JE ,dtype = np.float64) ],
           'JiE': [np.mean(JiE,dtype = np.float64)],
           'JeE': [np.mean(JeE,dtype = np.float64)],
           })

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