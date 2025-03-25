import TurbPy as tb
from TurbPy.imports import *

deck = 'KH_200ppc_200wci/'
dirs = '/pscratch/sd/g/goodwill/' + deck
figs = '/pscratch/sd/g/goodwill/Fig/' + deck

info = tb.get_vpic_info(dirs)
times = tb.get_times(dirs)
en_out = tb.read_energies(dirs)/(info['Lx/de'] * info['Ly/de'] * info['Lz/de'])

twci_out = np.linspace(0, times[-1] * info['dt*wci'], len(en_out['EM']))
twci = np.linspace(0, times[-1] * info['dt*wci'], len(times))

twce_out = np.linspace(0, times[-1] * info['dt*wce'], len(en_out['EM']))
twce = np.linspace(0, times[-1] * info['dt*wce'], len(times))

lx = np.linspace(0, info['Lx/di'], int(info['nx']))
ly = np.linspace(0, info['Ly/di'], int(info['ny']))

snaps = [300, 507, 652, 1087]
print(twci[snaps])

def time_av(t, num = 10):
  # pthe_t, pide_t = tb.ps_calc(dirs, times[t], 'electron')
  # el = tb.load_hydro_fil(dirs, times[t], 'electron')
  # ion = tb.load_hydro_fil(dirs, times[t], 'ion')
  # j_t = np.sqrt((el['jx'] + ion['jx'])**2  + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
  # wex, wey, wez = tb.w_calc(dirs, t, 'electron')
  # we_t = np.sqrt(wex**2 + wey**2 + wez**2)
  sh = np.zeros((int(info['nx']), int(info['ny'])))
  pthe = sh
  pide = sh
  pthi = sh
  pidi = sh
  JiE = sh
  JeE = sh
  JE = sh
  j = sh
  we = sh
  # pthe = np.zeros(pthe_t.shape)
  # pide = np.zeros(pide_t.shape)
  # # pthi_t, pidi_t = tb.ps_calc(dirs, times[t], 'ion')
  # pthi = np.zeros(pthi_t.shape)
  # pidi = np.zeros(pidi_t.shape)
  # JiE_t, JeE_t, JE_t = tb.JE_calc(dirs, times[t])
  # JiE = np.zeros(JE_t.shape)
  # JeE = np.zeros(JE_t.shape)
  # JE = np.zeros(JE_t.shape)
  # j = np.zeros(j_t.shape)
  # we = np.zeros(we_t.shape)
  for i in np.arange(int(-(num/2)), int(num/2)+1):
    el = tb.load_hydro_fil(dirs, times[t + i], 'electron')
    ion = tb.load_hydro_fil(dirs, times[t + i], 'ion')
    j_t = (el['jx'] + ion['jx'])**2  + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2
    wex, wey, wez = tb.w_calc(dirs, t, 'electron')
    we_t = np.sqrt(wex**2 + wey**2 + wez**2)
    pthe_t, pide_t = tb.ps_calc(dirs, times[t + i], 'electron')
    pthi_t, pidi_t = tb.ps_calc(dirs, times[t + i], 'ion')
    pthe = pthe + pthe_t
    pthi = pthi + pthi_t
    pide = pide + pide_t
    pidi = pidi + pidi_t
    JiE_t, JeE_t, JE_t = tb.JE_calc(dirs, times[t + i])
    JiE = JiE + JiE_t
    JeE = JeE + JeE_t
    JE = JE + JE_t
    j = j + j_t
    we = we + we_t
  we = we/num
  j = j/num
  JE = JE/num
  pthe = pthe/num
  pide = pide/num
  pthi = pthi/num
  pidi = pidi/num

  return j, JE, pthe, pide, pthi
  # return j, JE, pthe, pide, pthi, pidi
# JE, pthe, pide, pthi, pidi = time_av(1087)

fig, axs = plt.subplots(6,4, figsize=(12, 10), sharex = True, sharey = True, layout = 'constrained')
# fig.subplots_adjust(wspace = 0.01, hspace = 0.01)
snaps = [300, 507, 652, 1087]
for i in np.arange(len(snaps)):
  t = snaps[i]
  print(twci[t])
  el = tb.load_hydro_fil(dirs, times[t], species = 'electron')
  ion = tb.load_hydro_fil(dirs, times[t], species = 'ion')
  f = tb.load_field_fil(dirs, times[t])

  # j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2 )
  # by = f['cby']
  we = tb.pcurl(el['jx']/el['rho'], el['jy']/el['rho'], el['jz']/el['rho'], dx = info['Lx/de']/info['nx'], dy = info['Ly/de']/info['ny'])
  we_abs = np.sqrt(we[0]**2 + we[1]**2 + we[2]**2)
  # JiE, JeE, JE = tb.JE_calc(dirs, times[t])
  # pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
  # pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')


  pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
  j, JE, pthe, pide, pthi = time_av(t)
  # j, JE, pthe, pide, pthi, pidi = time_av(t)
  
  hot = 'afmhot'
  seis = 'seismic'
  cm1 = axs[0,i].pcolormesh(ly,lx,j, cmap = hot, vmin = 0, vmax = np.max(j)) 
  cm2 = axs[1,i].pcolormesh(ly,lx,we_abs, cmap = hot,  vmin = 0, vmax = np.max(we_abs)) 
  cm3 = axs[2,i].pcolormesh(ly,lx,JE, cmap = seis, vmin = -np.max(JE), vmax = np.max(JE)) 
  cm4 = axs[3,i].pcolormesh(ly,lx, pide, cmap = seis,  vmin = -np.max(pide), vmax = np.max(pide)) 
  # cm5 = axs[4,i].pcolormesh(ly,lx, pthe, cmap = seis,  vmin = -np.max(pthe), vmax = np.max(pthe))
  cm6 = axs[4,i].pcolormesh(ly,lx, pidi, cmap = seis,  vmin = -np.max(pidi)/7, vmax = np.max(pidi)/7) 
  cm7 = axs[5,i].pcolormesh(ly,lx, pthi, cmap = seis,  vmin = -np.max(pthi), vmax = np.max(pthi))

  axs[0,i].tick_params(left = False, right = False, top = False, bottom = False)
  axs[1,i].tick_params(left = False, right = False, top = False, bottom = False)
  axs[2,i].tick_params(left = False, right = False, top = False, bottom = False)
  axs[3,i].tick_params(left = False, right = False, top = False, bottom = False)
  # axs[4,i].tick_params(left = False, right = False, top = False, bottom = False)
  axs[4,i].tick_params(left = False, right = False, top = False, bottom = False)
  axs[5,i].tick_params(left = False, right = False, top = False, bottom = False)

  axs[3,i].text(0.1,11, r'$\langle PiD^e\rangle = $'f'{np.format_float_scientific(np.average(pide), precision = 2)}')
  # axs[4,i].text(0.1,11, r'$\langle p \theta^e\rangle = $'f'{np.format_float_scientific(np.average(pthe), precision = 2)}')
  axs[4,i].text(0.1,11, r'$\langle PiD^i\rangle = $'f'{np.format_float_scientific(np.average(pidi), precision = 2)}')
  axs[5,i].text(0.1,11, r'$\langle p \theta^i\rangle = $'f'{np.format_float_scientific(np.average(pthi), precision = 2)}')



  if i == len(snaps)-1:
    cb1 = fig.colorbar(cm1 , ax = axs[0,i], shrink = 0.7, format = '%.0E')
    cb2 = fig.colorbar(cm2 , ax=  axs[1,i], shrink = 0.7, format = '%.0E')
    cb3 = fig.colorbar(cm3 , ax = axs[2,i], shrink = 0.7, format = '%.0E')
    cb4 = fig.colorbar(cm4 , ax = axs[3,i], shrink = 0.7, format = '%.0E')
    # cb5 = fig.colorbar(cm5 , ax = axs[4,i], shrink = 0.7, format = '%.0E')
    cb6 = fig.colorbar(cm6 , ax = axs[4,i], shrink = 0.7, format = '%.0E')
    cb7 = fig.colorbar(cm7 , ax = axs[5,i], shrink = 0.7, format = '%.0E')

cb1.ax.set_title('|J|')
cb2.ax.set_title(r'|$\omega^e$|')
cb3.ax.set_title(r'$j \cdot E$')
cb4.ax.set_title(r'$PiD^e$')
# cb5.ax.set_title(r'$p \theta^e$')
cb6.ax.set_title(r'$PiD^i$')
cb7.ax.set_title(r'$p \theta^i$')
axs[0,0].set_title(r'Phase I')
axs[0,1].set_title(r'Phase II')
axs[0,2].set_title(r'Phase III')
axs[0,3].set_title(r'Phase IV')

fig.supxlabel(r'$L_y (d_i)$')
fig.supylabel(r'$L_x (d_i)$')

plt.savefig(figs + 'snaps.png', bbox_inches = 'tight', pad_inches = 0)
fig.clf()
