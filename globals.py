from .load_vars import *
from .pderiv import *
from .vpic_info import *
import pandas as pd

def globals(dirs):
  info = get_vpic_info(dirs)
  times = get_times(dirs)
  jrms_t = np.array([])
  drhoe_t = np.array([])
  drhoi_t = np.array([])
  db_t = np.array([])
  ome_t = np.array([])
  omi_t = np.array([])
  for t in np.arange(0,len(times)):
    dse = load_vars(dirs, times[t], species = 'electron')
    dsi = load_vars(dirs, times[t], species = 'ion')
    jx = (dse['jx'] + dsi['jx'])
    jy = (dse['jy'] + dsi['jy'])
    jz = (dse['jz'] + dsi['jz'])
    jrms_t = np.append(jrms_t, np.sqrt(np.average(jx**2 + jy**2 + jz**2)))
    drhoe_t = np.append(drhoe_t, np.sqrt(np.average((dse['rho']- np.average(dse['rho']))**2)))
    drhoi_t = np.append(drhoi_t, np.sqrt(np.average((dsi['rho']- np.average(dsi['rho']))**2)))
    db_t = np.append(db_t, 
                      np.sqrt(np.average((dse['cbx'] - np.average(dse['cbx']))**2)+
                      np.average((dse['cby'] - np.average(dse['cby']))**2) +
                      np.average((dse['cbz'] - np.average(dse['cbz']))**2)))
    ome = pcurl(dse['jx']/dse['rho'],
                  dse['jy']/dse['rho'], 
                  dse['jz']/dse['rho'], 
                  dx = info['dx/de'], 
                  dy = info['dy/de'], 
                  dz = info['dz/de'])
    omi = pcurl(dsi['jx']/dsi['rho'],
                  dsi['jy']/dsi['rho'], 
                  dsi['jz']/dsi['rho'], 
                  dx = info['dx/de'], 
                  dy = info['dy/de'], 
                  dz = info['dz/de'])
    ome_t = np.append(ome_t, np.sqrt(np.average(ome[0]**2 + ome[1]**2 + ome[2]**2)))
    omi_t = np.append(omi_t, np.sqrt(np.average(omi[0]**2 + omi[1]**2 + omi[2]**2)))

    df = pd.DataFrame({'jrms': jrms_t, 
                      'drhoi': drhoi_t,
                      'drhoe': drhoe_t,
                      'db': db_t,
                      'ome': ome_t,
                      'omi': omi_t})
    df.to_csv(dirs + 'data/' + 'globals.csv')
    return