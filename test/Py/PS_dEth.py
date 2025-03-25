import TurbPy as tb
from TurbPy.imports import *

# deck = 'KH_Lv1di/'
# deck  = 'KH/'
# deck = 'KH_subash/'
# deck = 'KH_new/'
# deck = 'KH_400ppc/'
deck = ''
# deck = 'KH_beta0.1/'
# deck = 'turb2/'
# deck = 'turb_vth0.01/'

dirs = '/pscratch/sd/g/goodwill/' + deck
figs = '/pscratch/sd/g/goodwill/Fig/' + deck

info = tb.get_vpic_info(dirs)
times = tb.get_times(dirs)
en_out = tb.read_energies(dirs)

twci_out = np.linspace(0, times[-1] * info['dt*wci'], len(en_out['EM']))
twce = np.linspace(0, times[-1] * info['dt*wce'], len(times))
twci = np.linspace(0, times[-1] * info['dt*wci'], len(times))

lx = info['Lx/di']
ly = info['Ly/di']
nx = int(info['nx'])
ny = int(info['ny'])

dt = info['dt*wpe'] * info['fields_interval']

## Calculate ###
# sp = 'electron'
# ps_av = tb.ps_av(dirs, sp)
# sp = 'ion'
# ps_av = tb.ps_av(dirs, sp)
# en = tb.en_calc(dirs)

### Read ###
en = tb.read_calc_energies(dirs)
n = 0
sp = 'electron'
dse = pd.read_csv(dirs + f'ps{sp[0]}_av.csv', delimiter = ',')
pse_av = dse[f'PS{sp[0]}']
dEthe = (en[f'Eth{sp[0]}'] - en[f'Eth{sp[0]}'][n])/((info['Lx/de'] * info['Ly/de'] * info['Lz/de']))

sp = 'ion'
dsi = pd.read_csv(dirs + f'ps{sp[0]}_av.csv', delimiter = ',')
psi_av = dsi[f'PS{sp[0]}']
dEthi = (en[f'Eth{sp[0]}'] - en[f'Eth{sp[0]}'][n])/((info['Lx/de'] * info['Ly/de'] * info['Lz/de']))

pse_int = sci.integrate.cumulative_trapezoid(pse_av * dt, initial = 0)
psi_int = sci.integrate.cumulative_trapezoid(psi_av * dt, initial = 0)

# pse_int = np.cumsum(pse_av) * dt
# psi_int = np.cumsum(psi_av) * dt

n = 0
time_twci = np.round(twci[n],1)
dpse = pse_int - pse_int[n]
dpsi = psi_int - psi_int[n]



fig, axs = plt.subplots(2,1, figsize=(15, 10), sharex = True, layout='constrained')
sp = 'ion'
axs[0].plot(twci, dpsi, marker = 'x', label = r'$\int_{'f'{time_twci}'r'}^t PS^'f'{sp[0]}'' dt$')
axs[0].plot(twci, dEthi,marker = 'x', label = r'$\delta E_{th}^'f'{sp[0]}''$')
axs[0].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[0].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[0].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[0].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[0].legend(title = sp, title_fontsize = 25, loc = 'upper left', fontsize = 20)
axs[0].xaxis.set_minor_locator(AutoMinorLocator())
axs[0].yaxis.set_minor_locator(AutoMinorLocator())
axs[0].tick_params(which='both', width=2, labelsize = 20, right = True, direction = 'in')
axs[0].tick_params(which='major', length=10, top = True, right =True)
axs[0].tick_params(which='minor', length=5 , top = True, right =True)
axs[0].grid()

sp = 'electron'
axs[1].plot(twci, dpse, marker = 'x', label = r'$\int_{'f'{time_twci}'r'}^t PS^'f'{sp[0]}'' dt$')
axs[1].plot(twci, dEthe,marker = 'x', label = r'$\delta E_{th}^'f'{sp[0]}''$')
axs[1].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[1].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[1].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[1].ticklabel_format(axis = 'y',style = 'sci', scilimits = (0,0))
axs[1].legend(title = sp, title_fontsize = 25, loc = 'upper left', fontsize = 20)
axs[1].xaxis.set_minor_locator(AutoMinorLocator())
axs[1].yaxis.set_minor_locator(AutoMinorLocator())
axs[1].tick_params(which='both', width=2, labelsize = 20, right = True, direction = 'in')
axs[1].tick_params(which='major', length=10, top = True, right =True)
axs[1].tick_params(which='minor', length=5 , top = True, right =True)
axs[1].grid()

fig.supylabel(r'$\delta E \left[ \frac{m_e c^2}{d_e^3} \right] $', size = 25)
fig.supxlabel(r'$ t \omega_{ci} \left[ \frac{e B_0}{m_i c} \right]$', size = 25)

plt.savefig(figs + 'PS_dEth.jpg', dpi = 400)