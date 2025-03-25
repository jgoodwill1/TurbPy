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

# K_pide = np.array([])
# K_pidi = np.array([])
# K_JE = np.array([])
# # twciC = twci[::50]
# for t in np.arange(0, len(times)):
#   print(twci[t])
#   f = tb.load_field_fil(dirs, times[t])
#   el = tb.load_hydro_fil(dirs, times[t], 'electron')
#   ion = tb.load_hydro_fil(dirs, times[t], 'ion')
#   JiE, JeE, JE = tb.JE_calc(dirs, times[t])
#   pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
#   pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
#   pide = tb.kfilter(pide, 5, lx = lx_de, ly = ly_de)
#   pidi = tb.kfilter(pidi, 5, lx = lx_de, ly = ly_de)
#   JE = tb.kfilter(JE, 5, lx = lx_de, ly = ly_de)
#   K_JE = np.append(K_JE,sci.stats.kurtosis(JE.flatten()))
#   K_pide = np.append(K_pide,sci.stats.kurtosis(pide.flatten()))
#   K_pidi = np.append(K_pidi,sci.stats.kurtosis(pidi.flatten()))
# np.savetxt(dirs + 'K_pide.csv', K_pide)
# np.savetxt(dirs + 'K_pidi.csv', K_pidi)
# np.savetxt(dirs + 'K_JE.csv', K_JE)


# plt.hist(pide, bins = 20)
# plt.legend()
# plt.ylim(0,2000)
# plt.xlim(0,155)
# plt.savefig(figs + 'pide_pdf.png')
# plt.close()

K_JE = np.loadtxt(dirs + 'K_JE.csv')
K_pide = np.loadtxt(dirs + 'K_pide.csv')
K_pidi = np.loadtxt(dirs + 'K_pidi.csv')

fig, ax = plt.subplots(layout = 'tight')

ax.plot(twci, K_JE+3, label = r'$K_{j \cdot E}$')
ax.plot(twci, K_pide+3, label = r'$K_{PiD^e}$')
ax.plot(twci, K_pidi+3, label = r'$K_{PiD^i}$')
ax.tick_params(labelsize = 18)
ax.legend()
ax.grid()
ax.set_ylim(0,500)
ax.set_xlim(0,155)
ax.set_xlabel(r'$t \omega_{ci}$', fontsize = 18)
fig.savefig(figs + 'kurt.png')
plt.close()