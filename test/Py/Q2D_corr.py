import TurbPy as tb
from TurbPy.imports import *
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, 
                               FormatStrFormatter, 
                               AutoMinorLocator) 

deck = 'KH_200ppc_200wci/'
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

nxc = 1080
nyc = 2560
lxr_di = np.linspace(0, lx_di, nxc)
lyr_di = np.linspace(0, ly_di, nyc)
lxr_de = np.linspace(0, lx_de, nxc)
lyr_de = np.linspace(0, ly_de, nyc)

dx = lx_de/nx
dy = ly_de/ny
s = 'seismic'
spec = 'turbo'
# tsnap = [290, 507, 657, 1124]
t = 507
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
QDe = tb.QD_calc(dirs, t, sp = 'electron')
QDi = tb.QD_calc(dirs, t, sp = 'ion')
Qwe = tb.Qw_calc(dirs, t, sp = 'electron')
Qwi = tb.Qw_calc(dirs, t, sp = 'ion')
QJe, QJi, QJ = tb.QJ_calc(dirs, t)


# gridspec = {'width_ratios': [1, 1 , 0.1]}
fig, axs = plt.subplots(4,2 , figsize = (20, 20), sharex = True, sharey = True)
cm00 = axs[0,0].pcolormesh(pide, cmap = s, vmin = -5e-5, vmax = 5e-5)
cm10 = axs[1,0].pcolormesh(QDe, cmap = spec, vmin = 0, vmax = 2)
cm20 = axs[2,0].pcolormesh(Qwe, cmap = spec, vmin = 0, vmax = 1)
cm30 = axs[3,0].pcolormesh(QJ, cmap = spec, vmin = 0, vmax = 2)


cm01 = axs[0,1].pcolormesh(pidi, cmap = s, vmin = -5e-6, vmax = 5e-6)
cm11 = axs[1,1].pcolormesh(QDi * 100, cmap = spec, vmin = 0, vmax = 2)
cm21 = axs[2,1].pcolormesh(Qwi * 5, cmap = spec, vmin = 0, vmax = 2)
cm31 = axs[3,1].pcolormesh(QJ, cmap = spec, vmin = 0, vmax = 2)

ft = 20
axs[0,0].set_title('PiDe', fontsize = ft)
axs[1,0].set_title('QDe' , fontsize = ft)
axs[2,0].set_title('Qwe' , fontsize = ft)
axs[3,0].set_title('QJ'  , fontsize = ft) 

axs[0,1].set_title('PiDi',fontsize = ft)
axs[1,1].set_title('100 * QDi' ,fontsize = ft)
axs[2,1].set_title('5 * Qwi' ,fontsize = ft)
axs[3,1].set_title('QJ'  ,fontsize = ft)

fig.colorbar(cm31, location = 'bottom')
fig.colorbar(cm30, location = 'bottom')


fig.savefig(figs + 'Q2D_corr_'f'{t}''.png')