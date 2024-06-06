import TurbPy as tb
from TurbPy.imports import *

# deck = 'KH_Lv1di/'
# deck = 'KH_new/'
# deck = 'KH_400ppc_200wci2/'
deck = 'KH_200ppc_200wci/'
# deck = 'KH_beta0.1/'
# deck = 'turb2/'

dirs = '/pscratch/sd/g/goodwill/' + deck
figs = '/pscratch/sd/g/goodwill/Fig/' + deck
info = tb.get_vpic_info(dirs)
times = tb.get_times(dirs)
en_out = tb.read_energies(dirs)
twci_out = np.linspace(0, times[-1] * info['dt*wci'], len(en_out['EM']))
twci = np.linspace(0, times[-1] * info['dt*wci'], len(times))
lx_de = info['Lx/de']
ly_de = info['Ly/de']
lx_di = info['Lx/di']
ly_di = info['Ly/di']
nx = int(info['nx'])
ny = int(info['ny'])
lxr_di = np.linspace(0, lx_di, nx)
lyr_di = np.linspace(0, ly_di, ny)
lxr_de = np.linspace(0, lx_de, nx)
lyr_de = np.linspace(0, ly_de, ny)
dx = lx_de/nx
dy = ly_de/ny

tsnap = [373, 507, 652, 1087]
fig, ax = plt.subplots(4,4, sharex = True, sharey = True, layout = 'tight')
y = 0
for t in tsnap:
  print(twci[t])
  f = tb.load_field_fil(dirs, times[t])
  el = tb.load_hydro_fil(dirs, times[t], 'electron')
  ion = tb.load_hydro_fil(dirs, times[t], 'ion')

  j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
  jrms = np.sqrt(np.mean(j**2))
  jnrm = j/jrms

  QJe, QJi, QJ = tb.QJ_calc(dirs, t)

  # QDe = tb.QD_calc(dirs, t, sp = 'electron')
  # QDi = tb.QD_calc(dirs, t, sp = 'ion')

  df = pd.DataFrame()
  emask = np.linspace(0, 15, 50)
  Jie, JeE, JE = tb.JE_calc(dirs, times[t])
  pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
  pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
  QDe_row = []
  tsize = 14
  # ax[y,0].pcolormesh(QDe, vmin = 0, vmax = 15)
  ax[y,0].pcolormesh(QJe, vmin = 0, vmax = 5)
  ax[y,1].pcolormesh(pide, cmap = 'seismic', vmin = -1e-4, vmax = 1e-4)
  # ax[y,2].pcolormesh(QDi, vmin = 0, vmax = 0.25)
  ax[y,2].pcolormesh(QJi, vmin = 0, vmax = 0.5)
  ax[y,3].pcolormesh(pidi, cmap = 'seismic', vmin = -1e-5, vmax = 1e-5)
  y = y + 1


fig.savefig(figs + 'QJ_mesh.png', dpi = 200)
fig.clf()