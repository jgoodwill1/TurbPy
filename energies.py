from .vpic_info import *
from .load_vars import *
import numpy as np
import pandas as pd


def read_energies(dirs):
  fdata = np.genfromtxt(dirs + "rundata/energies", skip_header=3)
  en_dict = {}
  ene_electric = np.sum(fdata[:, 1:4], axis=1)
  ene_magnetic = np.sum(fdata[:, 4:7], axis=1)
  ene_ion = fdata[:, 7]
  ene_electron = fdata[:, 8]
  ene_tot = np.sum(fdata[:, 1:], axis=1)

  en_dict['EE'] = ene_electric
  en_dict['EM'] = ene_magnetic
  en_dict['Ei'] = ene_ion
  en_dict['Ee'] = ene_electron
  en_dict['Et'] = ene_tot
  return pd.DataFrame(en_dict)

def read_calc_energies(dirs):
  fdata = pd.read_csv(dirs + 'en_calc.csv')

  en_dict = {}
  en_dict['EE'] = fdata['EE']
  en_dict['EM'] = fdata['EM']

  en_dict['Ethi'] = fdata['Ethi']
  en_dict['Efi'] = fdata['Efi']
  en_dict['Ei'] = fdata['Efi'] + fdata['Ethi']

  en_dict['Ethe'] = fdata['Ethe']
  en_dict['Efe'] = fdata['Efe']
  en_dict['Ee']  = fdata['Efe'] + fdata['Ethe']
  
  en_dict['Et'] = fdata['Et']
  return pd.DataFrame(en_dict)


def en_calc(dirs, save = True):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)
  en = {}
  
  E_fe = np.zeros(len(times))
  E_the = np.zeros(len(times))
  E_fi = np.zeros(len(times))
  E_thi = np.zeros(len(times))
  E_m = np.zeros(len(times))
  E_e = np.zeros(len(times))

  for t in np.arange(len(times)):
    dx = vpic_info['dx/de']
    dy = vpic_info['dy/de']
    dz = vpic_info['dz/de']
    ds = load_vars(dirs,times[t], 'ion')
    E_m[t] = (1/2) * np.sum(ds['cbx']**2 + ds['cby']**2 + ds['cbz']**2) * dx * dy *dz
    E_e[t] = (1/2) * np.sum(ds['ex']**2 + ds['ey']**2 + ds['ez']**2) * dx * dy * dz

    particle_mass = int(vpic_info['mi/me'])
    pxx = np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px'])
    pyy = np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py'])
    pzz = np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz'])
    
    ux=ds['jx']/ds['rho']
    uy=ds['jy']/ds['rho']
    uz=ds['jz']/ds['rho']

    E_thi[t] = (1/2) * np.sum(pxx + pyy + pzz) * dx * dy * dz
    E_fi[t]  = (1/2) * particle_mass  * np.sum( np.abs(ds['rho']) * (ux**2 + uy**2 + uz**2)) * dx * dy * dz

    ds = load_vars(dirs,times[t], 'electron')
    particle_mass = 1
    pxx = np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px'])
    pyy = np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py'])
    pzz = np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz'])
    
    ux=ds['jx']/ds['rho']
    uy=ds['jy']/ds['rho']
    uz=ds['jz']/ds['rho']

    E_the[t] = (1/2) * np.sum(pxx + pyy + pzz) * dx * dy * dz
    E_fe[t]  = (1/2) * particle_mass  * np.sum( np.abs(ds['rho']) * (ux**2 + uy**2 + uz**2)) * dx * dy * dz

  en['EM'] = E_m
  en['EE'] = E_e
  en['Ethi'] = E_thi
  en['Efi'] = E_fi
  en['Ethe'] = E_the
  en['Efe'] = E_fe
  en['Et'] = E_m + E_e + E_thi + E_fi + E_the + E_fe
  if save == True:
    pd.DataFrame(en).to_csv(dirs + 'en_calc.csv', sep = ',')
  return pd.DataFrame(en)

def EM_calc(dirs):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)
  en = {}
  
  E_m = np.zeros(len(times))
  E_e = np.zeros(len(times))

  for t in np.arange(len(times)):
    dx = vpic_info['dx/de']
    dy = vpic_info['dy/de']
    dz = vpic_info['dz/de']
    ds = load_vars(dirs,times[t])
    E_m[t] = (1/2) * np.sum(ds['cbx']**2 + ds['cby']**2 + ds['cbz']**2) * dx * dy *dz
    E_e[t] = (1/2) * np.sum(ds['ex']**2 + ds['ey']**2 + ds['ez']**2) * dx * dy * dz
  en['EM'] = E_m
  en['EE'] = E_e
  return pd.DataFrame(en)

def ion_calc(dirs):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)
  en = {}
  E_fi = np.zeros(len(times))
  E_thi = np.zeros(len(times))


  for t in np.arange(len(times)):
    dx = vpic_info['dx/de']
    dy = vpic_info['dy/de']
    dz = vpic_info['dz/de']
    ds = load_vars(dirs,times[t], 'ion')

    particle_mass = int(vpic_info['mi/me'])
    pxx = np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px'])
    pyy = np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py'])
    pzz = np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz'])
    
    ux=ds['jx']/ds['rho']
    uy=ds['jy']/ds['rho']
    uz=ds['jz']/ds['rho']

    E_thi[t] = (1/2) * np.sum(pxx + pyy + pzz) * dx * dy * dz
    E_fi[t]  = (1/2) * particle_mass  * np.sum( np.abs(ds['rho']) * (ux**2 + uy**2 + uz**2)) * dx * dy * dz
  
  en['Ethi'] = E_thi
  en['Efi'] = E_fi
  return pd.DataFrame(en)

def electron_calc(dirs):
  vpic_info = get_vpic_info(dirs)
  times = get_times(dirs)
  en = {}
  
  E_fe = np.zeros(len(times))
  E_the = np.zeros(len(times))

  for t in np.arange(len(times)):
    dx = vpic_info['dx/de']
    dy = vpic_info['dy/de']
    dz = vpic_info['dz/de']

    ds = load_vars(dirs,times[t], 'electron')
    particle_mass = 1
    pxx = np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px'])
    pyy = np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py'])
    pzz = np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz'])
    
    ux=ds['jx']/ds['rho']
    uy=ds['jy']/ds['rho']
    uz=ds['jz']/ds['rho']

    E_the[t] = (1/2) * np.sum(pxx + pyy + pzz) * dx * dy * dz
    E_fe[t]  = (1/2) * particle_mass  * np.sum( np.abs(ds['rho']) * (ux**2 + uy**2 + uz**2)) * dx * dy * dz

  en['Ethe'] = E_the
  en['Efe'] = E_fe
  return pd.DataFrame(en)