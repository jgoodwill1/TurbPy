from .load_vars import *
from .pderiv import *
from .vpic_info import *

def w_calc(dirs, t, sp = 'electron'):
  info = get_vpic_info(dirs)
  times = get_times(dirs)
  # dse = load_vars(dirs, times[t], species = sp)
  dse = load_hydro_fil(dirs, times[t], sp)
  ux = (dse['jx']/dse['rho'])[100:1180,:]
  uy = (dse['jy']/dse['rho'])[100:1180,:]
  uz = (dse['jz']/dse['rho'])[100:1180,:]
  om = pcurl(
        ux,
        uy, 
        uz, 
        dx = info['dx/de'], 
        dy = info['dy/de'], 
        dz = info['dz/de'])
  return np.array([om[0], om[1], om[2]])