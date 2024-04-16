from .vpic_info import *
from .kfilter import *
from .pderiv import *
from .load_vars import* 
import numpy as np
import pandas as pd

def ps_calc(dirs, timestep, species, kfilt = True, norm = False):
    if kfilt == True:
      ds = load_hydro_fil(dirs,timestep,species)
    else:
      ds = load_hydro(dirs,timestep,species)
    vpic_info = get_vpic_info(dirs)

    dx = vpic_info['dx/de']
    dy = vpic_info['dy/de']
    mi_me = vpic_info['mi/me']


    ux = ds['jx']/ds['rho']
    uy = ds['jy']/ds['rho']
    uz = ds['jz']/ds['rho']

    # pxx = np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px'])
    # pyy = np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py'])
    # pzz = np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz'])
    # pxy = np.array(ds['txy'] - (ds['jx']/ds['rho'])*ds['py'])


    # pxx = np.array(ds['txx'] - ux*ds['px'])
    # pyy = np.array(ds['tyy'] - uy*ds['py'])
    # pzz = np.array(ds['tzz'] - uz*ds['pz'])
    # pxy = np.array(ds['txy'] - ()*ds['py'])
    pxx = ds['txx'] - ux*ds['px']; pyy = ds['tyy'] - uy*ds['py']; pzz = ds['tzz'] - uz*ds['pz']
    pxy = ds['txy'] - ux*ds['py']; pxz = ds['tzx'] - ux*ds['pz']; pyz = ds['tyz'] - uy*ds['pz']
    # pyx = ds['txy'] - uy*ds['px']; pzx = ds['tzx'] - uz*ds['px']; pzy = ds['tyz'] - uz*ds['py']
    # pyx = np.array(txy - (jy/rho)*px)
    # pxz = np.array(ds['tzx'] - (ds['jx']/ds['rho'])*ds['pz'])
    # pzx = np.array(tzx - (jz/rho)*px)
    # pyz = np.array(ds['tyz'] - (ds['jy']/ds['rho'])*ds['pz'])
    # pzy = np.array(tyz - (jz/rho)*py)
    # if kfilt != None:
    #     pxx = kfilter(np.array(ds['txx'] - (ds['jx']/ds['rho'])*ds['px']), kfilt)
    #     pyy = kfilter(np.array(ds['tyy'] - (ds['jy']/ds['rho'])*ds['py']), kfilt)
    #     pzz = kfilter(np.array(ds['tzz'] - (ds['jz']/ds['rho'])*ds['pz']), kfilt)
    #     pxy = kfilter(np.array(ds['txy'] - (ds['jx']/ds['rho'])*ds['py']), kfilt)
    #     pxz = kfilter(np.array(ds['tzx'] - (ds['jz']/ds['rho'])*ds['px']), kfilt)
    #     pyz = kfilter(np.array(ds['tyz'] - (ds['jy']/ds['rho'])*ds['pz']), kfilt)



    # particle_mass = 1
    # if species == 'ion':
    #     particle_mass = mi_me
    #     ux=ds['jx']/ds['rho']
    #     uy=ds['jy']/ds['rho']
    #     uz=ds['jz']/ds['rho']
        # ux = ds['px']/np.abs(ds['rho'])/particle_mass
        # uy = ds['py']/np.abs(ds['rho'])/particle_mass
        # uz = ds['pz']/np.abs(ds['rho'])/particle_mass
    # if species == 'electron':
    #     particle_mass = 1
    #     ux=ds['jx']/ds['rho']
    #     uy=ds['jy']/ds['rho']
    #     uz=ds['jz']/ds['rho']
        # ux = ds['px']/np.abs(ds['rho'])/particle_mass
        # uy = ds['py']/np.abs(ds['rho'])/particle_mass
        # uz = ds['pz']/np.abs(ds['rho'])/particle_mass
    # if kfilt != None:
    #     ux = kfilter(ds['px']/np.abs(ds['rho'])/particle_mass, kfilt)
    #     uy = kfilter(ds['py']/np.abs(ds['rho'])/particle_mass, kfilt)
    #     uz = kfilter(ds['pz']/np.abs(ds['rho'])/particle_mass, kfilt)

    dux_dx = pderiv(ux,dx=dx,ax=0,order=2,smth=None)
    duy_dx = pderiv(uy,dx=dx,ax=0,order=2,smth=None)
    duz_dx = pderiv(uz,dx=dx,ax=0,order=2,smth=None)
    dux_dy = pderiv(ux,dx=dy,ax=1,order=2,smth=None)
    duy_dy = pderiv(uy,dx=dy,ax=1,order=2,smth=None)
    duz_dy = pderiv(uz,dx=dy,ax=1,order=2,smth=None)    

    
    # dux_dx = (np.roll(ux,-1,axis=0)-np.roll(ux,1,axis=0))/(2 * dx)
    # duy_dx = (np.roll(uy,-1,axis=0)-np.roll(uy,1,axis=0))/(2 * dx)
    # duz_dx = (np.roll(uz,-1,axis=0)-np.roll(uz,1,axis=0))/(2 * dx)
    
    # dux_dy = (np.roll(ux,-1,axis=1)-np.roll(ux,1,axis=1))/(2 * dy)
    # duy_dy = (np.roll(uy,-1,axis=1)-np.roll(uy,1,axis=1))/(2 * dy)
    # duz_dy = (np.roll(uz,-1,axis=1)-np.roll(uz,1,axis=1))/(2 * dy)

    theta = np.array(dux_dx + duy_dy)

    Dxx = np.array(dux_dx) - (1/3)*theta 

    Dyy = np.array(duy_dy) - (1/3)*theta
    Dzz = 0 - (1/3)*theta
    
    Dxy = np.array((1/2)*(dux_dy + duy_dx))
    Dxz = np.array((1/2)*(duz_dx))
    Dyz = np.array((1/2)*(duz_dy))

    p = np.array(pxx + pyy + pzz)/3
    PIxx = pxx - p
    PIyy = pyy - p
    PIzz = pzz - p
    ptheta = - p * theta
    pid = -(PIxx*Dxx+PIyy*Dyy+PIzz*Dzz+ 2.* np.array(pxy*Dxy+pxz*Dxz+pyz*Dyz))
    if norm == True:
        pid_rms = np.sqrt(np.mean(pid**2))
        pid = pid/pid_rms

        pth_rms = np.sqrt(np.mean(ptheta**2))
        ptheta = ptheta/pth_rms
    return ptheta, pid

def ps_av(dirs, sp = 'electron', n = False, save = True):
  times = get_times(dirs)
  ps_av  = np.zeros(len(times))
  pid_av = np.zeros(len(times))
  pth_av = np.zeros(len(times))
  for t in np.arange(len(times)):
    pth, pid = ps_calc(dirs, times[t], sp , norm = False)
    ps = pth + pid
    pid_av[t] = np.average(pid)
    pth_av[t] = np.average(pth)
    # psi = psi/psi_rms
    ps_av[t] = pid_av[t] + pth_av[t]
  if save == True:
    pd.DataFrame({f'PS{sp[0]}': ps_av}).to_csv(dirs + f'ps{sp[0]}_av.csv', sep = ',')
  return ps_av