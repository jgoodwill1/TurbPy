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

tsnap = [510, 657, 1124]
x = 0
y = 0
fig, ax = plt.subplots(3,2, figsize = (15, 20), sharex = 'col', layout = 'constrained')
# fig.subplots()
# subfigs = fig.subfigures(3,2)
# print(ax.shape)
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

  QJe, QJi, QJ = tb.QJ_calc(dirs, t)

  Qwe = tb.Qw_calc(dirs, t, sp = 'electron')
  Qwi = tb.Qw_calc(dirs, t, sp = 'ion')

  df = pd.DataFrame()
  emask = np.linspace(0, 1.75, 50)
  Jie, JeE, JE = tb.JE_calc(dirs, times[t])
  pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
  pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
 

  pid_rat = np.average(pidi)/np.average(pide)
  Qe_row = []
  tsize = 14
  for fn in emask:  
    QDe_thres = np.where(QDe > fn)
    QJe_thres = np.where(QJ > fn)
    Qwe_thres = np.where(Qwe > fn)
    
    # JE_QDe =   np.average(JE[QDe_thres])
    pide_QDe = np.average(pide[QDe_thres])
    pidi_QDe = np.average(pidi[QDe_thres])
    pidi_QDe = pidi_QDe / pid_rat
    pide_Qwe = np.average(pide[Qwe_thres])
    pidi_QJe = np.average(pidi[QJe_thres])
    
    pide_QJe = np.average(pide[QJe_thres])
    QJe_cnt = len(QJe_thres[0])
    Qwe_cnt = len(Qwe_thres[0])
    QDe_cnt = len(QDe_thres[0])
    Qe_row.append({
      'QJe': QJe_cnt, 
      'Qwe': Qwe_cnt,
      'QDe': QDe_cnt,
      'pide_Qwe': pide_Qwe,
      'pide_QDe': pide_QDe, 
      'pidi_QDe': pidi_QDe, 
      'pide_QJe': pide_QJe, 
      # 'pidi_QJe': pidi_QJe
      })
  # df =pd.DataFrame(row)
  Qi_row = []
  imask = np.linspace(0, 0.020, 50)
  for ifn in imask:  
    QDi_thres = np.where(QDi > ifn)
    QJi_thres = np.where(QJ > ifn)
    Qwi_thres = np.where(Qwi > ifn)
    # JE_QDi =   np.average(JE[QDi_thres])
    pidi_QDi = np.average(pidi[QDi_thres])
    pidi_Qwi = np.average(pidi[Qwi_thres])
    pide_QDi = np.average(pide[QDi_thres])
    pide_QDi = pide_QDi * pid_rat
    pidi_QJi = np.average(pidi[QJi_thres])
    # pide_QJi = np.average(pide[QJi_thres])
    QJi_cnt = len(QJi_thres[0])
    Qwi_cnt = len(Qwi_thres[0])
    QDi_cnt = len(QDi_thres[0])
    Qi_row.append({
      'QJi': QJi_cnt, 
      'Qwi': Qwi_cnt,
      'QDi': QDi_cnt,
      'pide_QDi': pide_QDi, 
      'pidi_Qwi': pidi_Qwi,
      'pidi_QDi': pidi_QDi,
      # 'pide_QJi': pide_QJi, 
      'pidi_QJi': pidi_QJi
      })
  Qe_cond = pd.DataFrame(Qe_row)
  Qi_cond = pd.DataFrame(Qi_row)
  df = pd.concat([Qe_cond, Qi_cond], axis = 1, join = 'inner')
  
  ax[x,y].plot(emask, df['pide_QDe'], marker = 'o', color = 'purple', label = r'$\langle PiD^e | Q_D^e\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].plot(emask, df['pide_Qwe'], marker = 's', color = 'indigo', label = r'$\langle PiD^e | Q_\omega^e\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].plot(emask, df['pide_QJe'], marker = 'x', color = 'violet', label = r'$\langle PiD^e | Q_J\rangle$', markersize = 4, linewidth = 3 )
  # ax[x,y].plot(emask, df['pidi_QDe'], color = 'red', label = r'$\langle PiD^i | Q_D^e\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].grid(which = 'both')
  ax[x,y].set_ylim(-5e-7, 1.25e-5)
  ax[x,y].yaxis.offsetText.set_fontsize(30)
  
  ax[x,y].set_xlim(0,1.75)
  # ax[x,y].set_title(r'$t \omega_{ci} = $'f'{np.round(twci[tsnap[x]],2)}', fontsize = 40)
  # ax2 = ax[y,x].twinx()
  # ax2.plot(emask, df['QDe'], linestyle = 'dashed', color = 'black')
  # ax2.plot(emask, df['Qwe'], linestyle = 'dashed', color = 'gray')
  # ax2.set_ylabel('Counts')
  # ax2.set_yscale('log')
  y = 1
  
  ax[x,y].plot(imask, df['pidi_QDi'], marker = 'o', color = 'red', label = r'$\langle PiD^i | Q_D^i\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].plot(imask, df['pidi_Qwi'], marker = 's', color = 'green', label = r'$\langle PiD^i | Q_\omega^i\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].plot(imask, df['pidi_QJi'], marker = 'x', color = 'blue', label = r'$\langle PiD^i | Q_J\rangle$', markersize = 4, linewidth = 3 )
  # ax[x,y].plot(imask, df['pide_QDi'], color = 'blue', label = r'$\langle PiD^e | Q_D^i\rangle$', markersize = 4, linewidth = 3 )
  ax[x,y].grid(which = 'both')
  ax[x,y].set_xlim(0,0.020)
  ax[x,y].set_ylim(-1e-7,2e-6)
  ax[x,y].yaxis.get_offset_text().set_fontsize(30)
  # ax2 = ax[y,x].twinx()
  # ax2.plot(imask, df['QDi'], linestyle = 'dashed', color = 'black')
  # ax2.plot(imask, df['Qwi'], linestyle = 'dashed', color = 'gray')
  # ax2.set_ylabel('Counts')
  # ax2.set_yscale('log')
  x = x + 1
  y = 0
# import matplotlib as mpl
# mpl.rcParams.update({'font.size': 25})


twcis = np.round(twci[tsnap],2)
# subfigs[0,0].suptitle('asdf')

ax[0,0].legend(loc = 'upper left', title = r'$t \omega_{ci} = 'f'{twcis[0]}$',title_fontsize = 40, fontsize = 30, frameon = False)
ax[0,1].legend(loc = 'upper left',fontsize = 30, frameon = False)
ax[0,0].tick_params(labelsize = 30)
ax[1,0].tick_params(labelsize = 30)
ax[2,0].tick_params(labelsize = 30)
# ax[3,0].tick_params(labelsize = 30)

ax[0,1].tick_params(labelsize = 30)
ax[1,1].tick_params(labelsize = 30)
ax[2,1].tick_params(labelsize = 30)



ax[1,0].legend('', loc = 'upper left', title = r'$t \omega_{ci} = 'f'{twcis[1]}$',title_fontsize = 40, frameon = False)
ax[2,0].legend('', loc = 'upper left', title = r'$t \omega_{ci} = 'f'{twcis[2]}$',title_fontsize = 40, frameon = False)
# ax[3,1].tick_params(labelsize = 30)
ax[0,0].set_title('electrons',fontsize = 40)
ax[0,1].set_title('ions',fontsize = 40)
ax[2,0].set_xlabel(r'$Q_{D,\omega}^e,Q_J$', fontsize = 40)
ax[2,1].set_xlabel(r'$Q_{D,\omega}^i,Q_J$', fontsize = 40)

fig.savefig(figs + 'Q_condAv.png', dpi = 200)
fig.clf()