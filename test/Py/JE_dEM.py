import TurbPy as tb
from TurbPy.imports import *

# deck = 'KH_Lv1di/'
# deck = 'KH/'
# deck = 'KH_subash/'
# deck = 'KH_new/'
deck = 'KH_400ppc/'
# deck = '/GEM_feb26/'
# deck = 'turb2/'
# deck = 'turb_vth0.01/'
# deck = 'KH_beta0.1/'

dirs = '/pscratch/sd/g/goodwill/' + deck
figs = '/pscratch/sd/g/goodwill/Fig/' + deck

info = tb.get_vpic_info(dirs)
times = tb.get_times(dirs)
en_out = tb.read_energies(dirs)

twci_out = np.linspace(0, times[-1] * info['dt*wci'], len(en_out['EM']))
twce = np.linspace(0, times[-1] * info['dt*wce'], len(times))
twpe = np.linspace(0, times[-1] * info['dt*wpe'], len(times))
twci = np.linspace(0, times[-1] * info['dt*wci'], len(times))

lx = info['Lx/di']
ly = info['Ly/di']
nx = int(info['nx'])
ny = int(info['ny'])
dt = info['dt*wce'] * info['fields_interval']

## Calculate ###
JE = tb.JE_calc(dirs)
en = tb.en_calc(dirs)

## Read ##
ds = tb.read_JE(dirs)
print(ds.keys())

en = tb.read_calc_energies(dirs)/(info['Lx/de'] * info['Ly/de'] * info['Lz/de'])

fig, axs = plt.subplots(1,1, figsize=(15, 10), sharex = True, layout='constrained')

axs.plot(twci, -sci.integrate.cumulative_trapezoid(ds['JE'] * dt, initial = 0), marker = 'x', label=r'$-\int_0^t \langle j\cdot E \rangle dt$')
# axs.plot(twci, -np.cumsum(ds['JE'] * dt), marker = 'x', label=r'$-\int_0^t \langle j\cdot E \rangle dt$')
axs.plot(twci, en['EM']-en['EM'][0]+en['EE']-en['EE'][0],marker = 'x', label=r'$\delta E^m$')
axs.ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs.ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs.ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs.ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs.legend(loc = 'upper left', fontsize = 20)
axs.xaxis.set_minor_locator(AutoMinorLocator())
axs.yaxis.set_minor_locator(AutoMinorLocator())
axs.tick_params(which='both', width=2, labelsize = 20, right = True, direction = 'in')
axs.tick_params(which='major', length=10, top = True, right =True)
axs.tick_params(which='minor', length=5 , top = True, right =True)
axs.grid()

fig.supylabel(r'$\delta E \left[ \frac{m_e c^2}{d_e^3} \right] $', size = 25)
fig.supxlabel(r'$ t \omega_{ci} \left[ \frac{e B_0}{m_i c} \right]$', size = 25)

plt.savefig(figs + 'JE_dEM.jpg', dpi = 400)