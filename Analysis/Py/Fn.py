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

t = 1100
print(twci[t])
f = tb.load_field_fil(dirs, times[t])
el = tb.load_hydro_fil(dirs, times[t], 'electron')
ion = tb.load_hydro_fil(dirs, times[t], 'ion')

j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
jrms = np.sqrt(np.mean(j**2))
jnrm = j/jrms

df = pd.DataFrame()
jmask = np.linspace(0, 5, 50)
Jie, JeE, JE = tb.JE_calc(dirs, times[t])
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
row = []
for fn in jmask:  
  jfil = np.where((jnrm > fn))
  JEfilM = np.where((jnrm > fn) & (JE < 0))
  pidifilM = np.where((jnrm > fn) & (pidi < 0))
  pidefilM = np.where((jnrm > fn) & (pide < 0))
  JEfrnM =   np.abs(np.sum(JE[JEfilM]))
  pidifrnM = np.abs(np.sum(pidi[pidifilM]))
  pidefrnM = np.abs(np.sum(pide[pidefilM]))

  JEfilP = np.where((jnrm > fn) & (JE > 0))
  pidifilP = np.where((jnrm > fn) & (pidi > 0))
  pidefilP = np.where((jnrm > fn) & (pide > 0))
  JEfrnP =   np.sum(JE[JEfilP])
  pidifrnP = np.sum(pidi[pidifilP])
  pidefrnP = np.sum(pide[pidefilP])
  jfrn = len(jfil[0])
  row.append({'jfrn': jfrn,'JEP': JEfrnP, 'pideP': pidefrnP, 'pidiP': pidifrnP, 'JEM': JEfrnM, 'pideM': pidefrnM, 'pidiM': pidifrnM})
df =pd.DataFrame(row)

fig, ax = plt.subplots(1,1)
ax.semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
ax.semilogy(jmask, df['JEP']/df['JEP'][0], marker = '^', color = 'blue', label = r'$J \cdot E^{(\plus)}/J \cdot E_{T}$', markersize = 2)
# ax[0].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label = r'$PiD_e^{(\plus)}/PiD_e^{T}$', markersize = 2)
# ax[0].semilogy(jmask, df['pidiP']/df['pidiP'][0], marker = 'x', color = 'black', label = r'$PiD_i^{(\plus)}/PiD^i_{T}$', markersize = 2)


# ax.semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
ax.semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label = r'$J \cdot E^{(\minus)}/J \cdot E_{T}$', markersize = 2)
# ax[1].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'red', label = r'$PiD_e^{(\minus)}/PiD_e^{T}$', markersize = 2)
# ax[1].semilogy(jmask, df['pidiM']/df['pidiM'][0], marker = 'x', color = 'black', label = r'$PiD_i^{(\minus)}/PiD^i_{T}$', markersize = 2)
# ax[1].legend()
# ax[1].grid(which = 'both')
ax.legend(title = r'$t \omega_{ci} =$'f'{np.round(twci[t])}')
ax.grid(which = 'both')

fig.supylabel(r'$F(n)$')
fig.supxlabel(r'$J/J_{rms}$')
fig.savefig(figs + 'Fn2.png', dpi = 200)
fig.clf()