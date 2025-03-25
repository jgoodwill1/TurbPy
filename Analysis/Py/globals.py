import TurbPy as tb
from TurbPy.imports import *

deck = 'KH_200ppc_200wci/'

dirs = '/pscratch/sd/g/goodwill/' + deck
data = dirs + 'data/'
figs = '/pscratch/sd/g/goodwill/Fig/' + deck

info = tb.get_vpic_info(dirs)
times = tb.get_times(dirs)
en_out = tb.read_energies(dirs)/(info['Lx/de'] * info['Ly/de'] * info['Lz/de'])

twci_out = np.linspace(0, times[-1] * info['dt*wci'], len(en_out['EM']))
twci = np.linspace(0, times[-1] * info['dt*wci'], len(times))

twce_out = np.linspace(0, times[-1] * info['dt*wce'], len(en_out['EM']))
twce = np.linspace(0, times[-1] * info['dt*wce'], len(times))

from TurbPy.load_vars import *

jrms_t = np.array([])
jx2_av = np.array([])
jy2_av = np.array([])
jz2_av = np.array([])
ue2_av = np.array([])
ui2_av = np.array([])
drhoe_t = np.array([])
drhoi_t = np.array([])
drho_t = np.array([])
db_t = np.array([])
ome_t = np.array([])
omi_t = np.array([])
omz2e_av = np.array([])
omz2i_av = np.array([])
t_ch = np.arange(500, 520, 1)
print(t_ch)
for t in np.arange(len(times)):
  dse = tb.load_hydro_fil(dirs, times[t], species = 'electron')
  dsi = tb.load_hydro_fil(dirs, times[t], species = 'ion')
  f = tb.load_field_fil(dirs, times[t])
  jx = (dse['jx'] + dsi['jx'])
  jy = (dse['jy'] + dsi['jy'])
  jz = (dse['jz'] + dsi['jz'])
  uxe = dse['jx']/dse['rho']
  uye = dse['jy']/dse['rho']
  uze = dse['jz']/dse['rho']
  uxi = dsi['jx']/dsi['rho']
  uyi = dsi['jy']/dsi['rho']
  uzi = dsi['jz']/dsi['rho']
  ue2_av = np.append(ue2_av, np.average(uxe**2 + uye**2 + uze**2))
  ui2_av = np.append(ui2_av, np.average(uxi**2 + uyi**2 + uzi**2))
  jrms_t = np.append(jrms_t, np.sqrt(np.average(jx**2 + jy**2 + jz**2)))
  jx2_av = np.append(jx2_av, np.average(jx**2))
  jy2_av = np.append(jy2_av, np.average(jy**2))
  jz2_av = np.append(jz2_av, np.average(jz**2))
  drhoe_t = np.append(drhoe_t, np.sqrt(np.average((dse['rho'])**2)))
  drhoi_t = np.append(drhoi_t, np.sqrt(np.average((dsi['rho'])**2)))
  db_t = np.append(db_t, 
                    np.sqrt(np.average((f['cbx'])**2)+
                    np.average((f['cby'])**2) +
                    np.average((f['cbz'])**2)))
  ome = tb.pcurl(uxe,
                uye, 
                uze, 
                dx = info['dx/de'], 
                dy = info['dy/de'], 
                dz = info['dz/de'])
  omi = tb.pcurl(uxi,
                uyi, 
                uzi, 
                dx = info['dx/de'], 
                dy = info['dy/de'], 
                dz = info['dz/de'])
  omi = omi[60:1220]
  # print(np.average(dsi['jz']))
  # print(np.average(ome[0]**2 + ome[1]**2 + ome[2]**2))
  # print(np.average(omi[0]**2 + omi[1]**2 + omi[2]**2))
  ome_abs = np.average(ome[0]**2 + ome[1]**2 + ome[2]**2)
  ome_t = np.append(ome_t, np.average(ome[0]**2 + ome[1]**2 + ome[2]**2))
  omi_t = np.append(omi_t, np.average(omi[0]**2 + omi[1]**2 + omi[2]**2))
  # omz2e_av = np.append(omz2e_av, np.average(ome[2]**2))
  # omz2i_av = np.append(omz2i_av, np.average(omi[2]**2))