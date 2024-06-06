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

tsnap = [373, 507, 652, 1120]
x = 0
y = 0
fig, ax = plt.subplots(4,2, figsize = (10, 10), sharex = 'col', layout = 'tight')
print(ax.shape)
for t in tsnap:
  print(twci[t])
  f = tb.load_field_fil(dirs, times[t])
  el = tb.load_hydro_fil(dirs, times[t], 'electron')
  ion = tb.load_hydro_fil(dirs, times[t], 'ion')

  j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
  jrms = np.sqrt(np.mean(j**2))
  jnrm = j/jrms

  QDe = tb.QD_calc(dirs, t, sp = 'electron')
  QDi = tb.QD_calc(dirs, t, sp = 'ion')

  df = pd.DataFrame()
  emask = np.linspace(0, 15, 50)
  Jie, JeE, JE = tb.JE_calc(dirs, times[t])
  pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
  pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
  QDe_row = []
  tsize = 14
  for fn in emask:  
    QDe_thres = np.where((QDe > fn))
    # JE_QDe =   np.average(JE[QDe_thres])
    pidi_QDe = np.average(pidi[QDe_thres])
    pide_QDe = np.average(pide[QDe_thres])
    QDe_frn = len(QDe_thres[0])
    QDe_row.append({'QDe': QDe_frn, 'pide_QDe': pide_QDe, 'pidi_QDe': pidi_QDe})
  # df =pd.DataFrame(row)
  QDi_row = []
  imask = np.linspace(0, 3, 50)
  for fn in imask:  
    QDi_thres = np.where(QDi > fn)
    # JE_QDi =   np.average(JE[QDi_thres])
    pidi_QDi = np.average(pidi[QDi_thres])
    pide_QDi = np.average(pide[QDi_thres])
    QDi_frn = len(QDi_thres[0])
    QDi_row.append({'QDi': QDi_frn, 'pide_QDi': pide_QDi, 'pidi_QDi': pidi_QDi})
  QDe_cond = pd.DataFrame(QDe_row)
  QDi_cond = pd.DataFrame(QDi_row)
  df = pd.concat([QDe_cond, QDi_cond], axis = 1, join = 'inner')
  # print(df)
  # ax.semilogy(mask, df['QD']/df['QD'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
  # ax[x,y].plot(emask, df['JE_QDe'], marker = '^', color = 'blue', label = r'$\langle J \cdot E | Q_D^e\rangle$', markersize = 4)
  ax[x,y].plot(emask, df['pide_QDe'], marker = 'o', color = 'purple', label = r'$\langle PiD^e | Q_D^e\rangle$', markersize = 4)
  ax[x,y].plot(emask, df['pidi_QDe'], marker = 'x', color = 'violet', label = r'$\langle PiD^i | Q_D^e\rangle$', markersize = 4)
  ax[x,y].grid(which = 'both')
  # ax[x,y].text(1, 4,  r'$t \omega_{ci} = $'f'{np.round(twci[t],2)}')
  ax[x,y].legend('', title = r'$t \omega_{ci} = $'f'{np.round(twci[t],2)}', title_fontsize = tsize, frameon = False, loc = 'upper left')
  y = 1
  # ax[x,y].plot(imask, df['JE_QDi'], marker = '^', color = 'red', label = r'$\langle J \cdot E | Q_D^i\rangle$', markersize = 4)
  ax[x,y].plot(imask, df['pide_QDi'], marker = 'o', color = 'maroon', label = r'$\langle PiD^e | Q_D^i\rangle$', markersize = 4)
  ax[x,y].plot(imask, df['pidi_QDi'], marker = 'x', color = 'salmon', label = r'$\langle PiD^i | Q_D^i\rangle$', markersize = 4)
  ax[x,y].legend('', frameon = False, loc = 'upper left')
  ax[x,y].grid(which = 'both')
  x = x + 1
  y = 0
ax[0,0].legend(loc = 'upper left', fontsize = 13, title = r'$t \omega_{ci} = $'f'{np.round(twci[tsnap[0]],2)}', title_fontsize = tsize, frameon = False)
ax[0,1].legend(loc = 'upper left', fontsize = 13, frameon = False)

ax[0,0].set_ylim(-0.5e-6, 2e-6)
ax[0,1].set_ylim(-1.5e-6, 2e-6)
# ax[0,1].set_ylim(-1e-7, 2e-6)
# ax[2,0].set_ylim(-3e-6, 2e-6)

ax[-1,0].set_xlabel(r'$Q_D^e$', fontsize = 18)
ax[-1,1].set_xlabel(r'$Q_D^i$', fontsize = 18)

fig.savefig(figs + 'QD_thres.png', dpi = 200)
fig.clf()