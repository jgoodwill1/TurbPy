import TurbPy as tb
from TurbPy.imports import *
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, 
                               FormatStrFormatter, 
                               AutoMinorLocator) 

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

# fig5, ax = plt.subplots(2, 2, sharex = 'row', constrained_layout=True)
fig5 = plt.figure(constrained_layout = True)
subfigs = fig5.subfigures(2, 1)

ax0 = subfigs[0].subplots(1, 2, sharex=True, sharey = True)
ax1 = subfigs[1].subplots(1, 2, sharex=True, sharey = True)

t = 510
print(twci[t])
f = tb.load_field_fil(dirs, times[t])
el = tb.load_hydro_fil(dirs, times[t], 'electron')
ion = tb.load_hydro_fil(dirs, times[t], 'ion')


wV = tb.w_calc(dirs, t, sp = 'electron')
w = np.sqrt(wV[0]**2 + wV[1]**2 + wV[2]**2)
j = w

jrms = np.sqrt(np.mean(j**2))
jnrm = (j/jrms)[100:1180,:]

df = pd.DataFrame()
jmask = np.linspace(0, 3, 50)
JiE, JeE, JE = tb.JE_calc(dirs, times[t])
JiE = JiE[100:1180,:]
JeE = JeE[100:1180,:]
JE =  JE[100:1180,:]
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
row = []
for fn in jmask:  
  jfil = np.where((jnrm > fn))
  JEfilM = np.where((jnrm > fn) & (JE < 0))
  pidifilM = np.where((jnrm > fn) & (pidi < 0))
  pidefilM = np.where((jnrm > fn) & (pide < 0))
  JEM =   np.sum(JE[JEfilM])
  pidiM = np.sum(pidi[pidifilM])
  pideM = np.sum(pide[pidefilM])

  JEfilP = np.where((jnrm > fn) & (JE > 0))
  pidifilP = np.where((jnrm > fn) & (pidi > 0))
  pidefilP = np.where((jnrm > fn) & (pide > 0))
  JEP =   np.sum(JE[JEfilP])
  pidiP = np.sum(pidi[pidifilP])
  pideP = np.sum(pide[pidefilP])
  jfrn = len(jfil[0])
  JEPcnt = np.size(JEfilP)
  JEMcnt = np.size(JEfilM)
  row.append({
              'jfrn': jfrn, 
              'JEPcnt' : JEPcnt, 
              'JEP': JEP, 
              'pideP': pideP, 
              'pidiP': pidiP, 
              'JEMcnt' : JEMcnt,
              'JEM': JEM, 
              'pideM': pideM, 
              'pidiM': pidiM
              })
df =pd.DataFrame(row)

ax0[0].semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
ax0[0].semilogy(jmask, np.abs(df['JEP'])/df['JEP'][0], marker = '^', color = 'blue', label = r'$j \cdot E^{(+)}$', markersize = 2)
ax0[0].semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label = r'$j \cdot E^{(-)}$', markersize = 2)
ax0[0].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label = r'$PiD_e^{(+)}$', markersize = 2)
ax0[0].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'maroon', label = r'$PiD_e^{(-)}$', markersize = 2)
ax0[0].set_title(r'$t \omega_{ci} =$'f'{np.round(twci[t],2)}', fontsize = 20)


t = 1120
print(twci[t])
f = tb.load_field_fil(dirs, times[t])
el = tb.load_hydro_fil(dirs, times[t], 'electron')
ion = tb.load_hydro_fil(dirs, times[t], 'ion')


wV = tb.w_calc(dirs, t, sp = 'electron')
w = np.sqrt(wV[0]**2 + wV[1]**2 + wV[2]**2)
j = w

jrms = np.sqrt(np.mean(j**2))
jnrm = (j/jrms)[100:1180,:]

df = pd.DataFrame()
jmask = np.linspace(0, 3, 50)
JiE, JeE, JE = tb.JE_calc(dirs, times[t])
JiE = JiE[100:1180,:]
JeE = JeE[100:1180,:]
JE =  JE[100:1180,:]
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
row = []
for fn in jmask:  
  jfil = np.where((jnrm > fn))
  JEfilM = np.where((jnrm > fn) & (JE < 0))
  pidifilM = np.where((jnrm > fn) & (pidi < 0))
  pidefilM = np.where((jnrm > fn) & (pide < 0))
  JEM =   np.sum(JE[JEfilM])
  pidiM = np.sum(pidi[pidifilM])
  pideM = np.sum(pide[pidefilM])

  JEfilP = np.where((jnrm > fn) & (JE > 0))
  pidifilP = np.where((jnrm > fn) & (pidi > 0))
  pidefilP = np.where((jnrm > fn) & (pide > 0))
  JEP =   np.sum(JE[JEfilP])
  pidiP = np.sum(pidi[pidifilP])
  pideP = np.sum(pide[pidefilP])
  jfrn = len(jfil[0])
  JEPcnt = np.size(JEfilP)
  JEMcnt = np.size(JEfilM)
  row.append({
              'jfrn': jfrn, 
              'JEPcnt' : JEPcnt, 
              'JEP': JEP, 
              'pideP': pideP, 
              'pidiP': pidiP, 
              'JEMcnt' : JEMcnt,
              'JEM': JEM, 
              'pideM': pideM, 
              'pidiM': pidiM
              })
df =pd.DataFrame(row)

ax0[1].semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label='_Hidden label', markersize = 2)
ax0[1].semilogy(jmask, np.abs(df['JEP'])/df['JEP'][0], marker = '^', color = 'blue', label='_Hidden label', markersize = 2)
ax0[1].semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label='_Hidden label', markersize = 2)
ax0[1].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label='_Hidden label', markersize = 2)
ax0[1].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'maroon', label='_Hidden label', markersize = 2)
ax0[1].set_title(r'$t \omega_{ci} =$'f'{np.round(twci[t],2)}', fontsize = 20)
x1 = np.linspace(0.1, 3, 200)
y1 = np.exp(- x1**2)
# ax0[0].semilogy(x1, y1, c = 'black', linestyle = 'dashed', linewidth = 3, label = r'$e^{-\omega^e}$')
ax0[1].semilogy(x1, y1, c = 'black', linestyle = 'dashed', linewidth = 3, label = r'$e^{-\omega_e^2}$')

t = 510
print(twci[t])
f = tb.load_field_fil(dirs, times[t])
el = tb.load_hydro_fil(dirs, times[t], 'electron')
ion = tb.load_hydro_fil(dirs, times[t], 'ion')
j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
# j = (el['jx'] + ion['jx']) + (el['jy'] + ion['jy']) + (el['jz'] + ion['jz'])
jrms = np.sqrt(np.mean(j**2))
jnrm = (j/jrms)[100:1180,:]

df = pd.DataFrame()
jmask = np.linspace(0, 4, 50)
JiE, JeE, JE = tb.JE_calc(dirs, times[t])
JiE = JiE[100:1180,:]
JeE = JeE[100:1180,:]
JE =  JE[100:1180,:]
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
row = []
for fn in jmask:  
  jfil = np.where((jnrm > fn))
  JEfilM = np.where((jnrm > fn) & (JE < 0))
  pidifilM = np.where((jnrm > fn) & (pidi < 0))
  pidefilM = np.where((jnrm > fn) & (pide < 0))
  JEM =   np.sum(JE[JEfilM])
  pidiM = np.sum(pidi[pidifilM])
  pideM = np.sum(pide[pidefilM])

  JEfilP = np.where((jnrm > fn) & (JE > 0))
  pidifilP = np.where((jnrm > fn) & (pidi > 0))
  pidefilP = np.where((jnrm > fn) & (pide > 0))
  JEP =   np.sum(JE[JEfilP])
  pidiP = np.sum(pidi[pidifilP])
  pideP = np.sum(pide[pidefilP])
  jfrn = len(jfil[0])
  JEPcnt = np.size(JEfilP)
  JEMcnt = np.size(JEfilM)
  row.append({
              'jfrn': jfrn, 
              'JEPcnt' : JEPcnt, 
              'JEP': JEP, 
              'pideP': pideP, 
              'pidiP': pidiP, 
              'JEMcnt' : JEMcnt,
              'JEM': JEM, 
              'pideM': pideM, 
              'pidiM': pidiM
              })
df =pd.DataFrame(row)

ax1[0].semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
ax1[0].semilogy(jmask, np.abs(df['JEP'])/df['JEP'][0], marker = '^', color = 'blue', label = r'$j \cdot E^{(+)}$', markersize = 2)
ax1[0].semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label = r'$j \cdot E^{(-)}$', markersize = 2)
ax1[0].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label = r'$PiD_e^{(+)}$', markersize = 2)
ax1[0].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'maroon', label = r'$PiD_e^{(-)}$', markersize = 2)


# fig = plt.figure()
# fig.subplots_adjust(hspace = 1e-1)
# fig.set_figheight(6)
# fig.set_figwidth(6)

# ax0 = plt.subplot2grid(shape = (5, 2), loc = (0,0))
# ax0.plot(jmask, df['JEP']/df['JEPcnt'], color = 'blue' ,label = r'$\langle j \cdot E^{(+)} | j \rangle$')
# ax0.plot(jmask, -df['JEM']/df['JEMcnt'],color = 'deepskyblue' ,label = r'$\langle j \cdot E^{(-)} | j \rangle$')
# ax0.set_ylim(5e-6, 6e-5)



# heights = [1, 3]
# spec5 = fig5.add_gridspec(ncols=2, nrows=2,
                          # height_ratios=heights)
# for row in range(3):
#     for col in range(3):
#         ax = fig5.add_subplot(spec5[row, col])
#         label = 'Width: {}\nHeight: {}'.format(heights[row])
#         ax.annotate(label, (0.1, 0.5), xycoords='axes fraction', va='center')


# ax = fig5.add_subplot(spec5[0, 0])
# ax1 = fig5.add_subplot(spec5[1, 0], sharex = ax)
# ax2 = fig5.add_subplot(spec5[0, 1], sharey = ax)
# ax3 = fig5.add_subplot(spec5[1, 1], sharex = ax2, sharey = ax1)
# ax1 = plt.subplot2grid(shape = (5, 2), loc = (1,0), rowspan = 4, sharex = ax0)
# ax1[0].semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label = 'Area', markersize = 2)
# ax1[0].semilogy(jmask, np.abs(df['JEP'])/df['JEP'][0], marker = '^', color = 'blue', label = r'$j \cdot E^{(+)}$', markersize = 2)
# ax1[0].semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label = r'$j \cdot E^{(-)}$', markersize = 2)
# ax1[0].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label = r'$PiD_e^{(+)}$', markersize = 2)
# ax1[0].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'maroon', label = r'$PiD_e^{(-)}$', markersize = 2)
# ax1.semilogy(jmask, df['pidiP']/df['pidiP'][0], marker = 'o', color = 'orange', label = r'$PiD_i^{(+)}/\langle PiD_i^{(+)}\rangle$', markersize = 2)
# ax1.semilogy(jmask, df['pidiM']/df['pidiM'][0], marker = 'o', color = 'sandybrown', label = r'$PiD_i^{(-)}/\langle PiD_i^{(-)}\rangle$', markersize = 2)
# ax1.semilogy(jmask, df['pidiP']/df['pidiP'][0], marker = '^', color = 'deepskyblue', label = r'$PiD_i^{(+)}/PiD_i^(+)$', markersize = 2)



# ax.plot(jmask, df['JEP']/df['JEPcnt'], color = 'blue' ,label = r'$\langle j \cdot E^{(+)} | j \rangle$')
# ax.plot(jmask, -df['JEM']/df['JEMcnt'],color = 'deepskyblue' ,label = r'$\langle j \cdot E^{(-)} | j \rangle$')
# ax.set_ylim(5e-6, 6e-5)

# ax1[0,0].set_title(r'$t \omega_{ci} =$'f'{np.round(twci[t],2)}', fontsize = 20)

t = 1120
print(twci[t])
f = tb.load_field_fil(dirs, times[t])
el = tb.load_hydro_fil(dirs, times[t], 'electron')
ion = tb.load_hydro_fil(dirs, times[t], 'ion')

j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
# j = (el['jx'] + ion['jx']) + (el['jy'] + ion['jy']) + (el['jz'] + ion['jz'])
jrms = np.sqrt(np.mean(j**2))

jnrm = (j/jrms)[100:1180,:]

df = pd.DataFrame()
jmask = np.linspace(0, 4, 50)
JiE, JeE, JE = tb.JE_calc(dirs, times[t])
JiE = JiE[100:1180,:]
JeE = JeE[100:1180,:]
JE =  JE[100:1180,:]
pthe, pide = tb.ps_calc(dirs, times[t], 'electron')
pthi, pidi = tb.ps_calc(dirs, times[t], 'ion')
row = []
for fn in jmask:  
  jfil = np.where((jnrm > fn))
  JEfilM = np.where((jnrm > fn) & (JE < 0))
  pidifilM = np.where((jnrm > fn) & (pidi < 0))
  pidefilM = np.where((jnrm > fn) & (pide < 0))
  JEM =   np.sum(JE[JEfilM])
  pidiM = np.sum(pidi[pidifilM])
  pideM = np.sum(pide[pidefilM])

  JEfilP = np.where((jnrm > fn) & (JE > 0))
  pidifilP = np.where((jnrm > fn) & (pidi > 0))
  pidefilP = np.where((jnrm > fn) & (pide > 0))
  JEP =   np.sum(JE[JEfilP])
  pidiP = np.sum(pidi[pidifilP])
  pideP = np.sum(pide[pidefilP])
  jfrn = len(jfil[0])
  JEPcnt = np.size(JEfilP)
  JEMcnt = np.size(JEfilM)
  row.append({
              'jfrn': jfrn, 
              'JEPcnt' : JEPcnt, 
              'JEP': JEP, 
              'pideP': pideP, 
              'pidiP': pidiP, 
              'JEMcnt' : JEMcnt,
              'JEM': JEM, 
              'pideM': pideM, 
              'pidiM': pidiM
              })
df =pd.DataFrame(row)



# ax3 = plt.subplot2grid(shape = (5, 2), loc = (1,1), rowspan = 4, sharey = ax1)
ax1[1].semilogy(jmask, df['jfrn']/df['jfrn'][0], marker = 's', color = 'green', label='_Hidden label', markersize = 2)
ax1[1].semilogy(jmask, np.abs(df['JEP'])/df['JEP'][0], marker = '^', color = 'blue', label='_Hidden label',markersize = 2)
ax1[1].semilogy(jmask, df['JEM']/df['JEM'][0], marker = '^', color = 'deepskyblue', label='_Hidden label', markersize = 2)
ax1[1].semilogy(jmask, df['pideP']/df['pideP'][0], marker = 'o', color = 'red', label='_Hidden label', markersize = 2)
ax1[1].semilogy(jmask, df['pideM']/df['pideM'][0], marker = 'o', color = 'maroon', label='_Hidden label', markersize = 2)
# ax3.semilogy(jmask, df['pidiP']/df['pidiP'][0], marker = 'o', color = 'orange', label = r'$PiD_i^{(+)}/\langle PiD_i^{(+)}\rangle$', markersize = 2)
# ax3.semilogy(jmask, df['pidiM']/df['pidiM'][0], marker = 'o', color = 'sandybrown', label = r'$PiD_i^{(-)}/\langle PiD_i^{(-)}\rangle$', markersize = 2)
# ax2 = plt.subplot2grid(shape = (5, 2), loc = (0,1), sharey = ax)
# ax2.plot(jmask, np.abs(df['JEP'])/df['JEPcnt'], color = 'blue' ,label = r'$\langle j \cdot E^{(+)} | j \rangle$')
# ax2.plot(jmask, np.abs(df['JEM'])/df['JEMcnt'],color = 'deepskyblue' ,label = r'$\langle j \cdot E^{(-)} | j \rangle$')
# ax1.set_ylim(5e-3, 1.5)

x1 = np.linspace(0.1, 4, 200)
y1 = np.exp(- 1.3 * x1)
ax1[1].semilogy(x1, y1, c = 'black', linestyle = 'dashed', linewidth = 3, label = r'$e^{-j}$')

# ax3.text(x1[40], y1[165], r'$4^{(-|j/j_{rms}|)}$', size = 20)
# ax0.yaxis.set_major_formatter(FormatStrFormatter('%.0E')) 


ax0[0].grid(which = 'both')
ax0[1].grid(which = 'both')
ax1[0].grid(which = 'both')
ax1[1].grid(which = 'both')

from matplotlib import pyplot as plt, ticker as mticker
ax0[0].yaxis.set_minor_locator(mticker.LogLocator(numticks=999, subs="auto"))

# ax[1,1].legend(frameon = False)
# ax2.grid(which = 'both')
# ax2.legend(frameon = False)
# ax2.set_title(r'$t \omega_{ci} =$'f'{np.round(twci[t],2)}', fontsize = 20)

# ax1.grid(which = 'both')
# ax3.grid(which = 'both')

# ax2.set_yticks([])
# ax3.set_yticks([])

# ax1.legend(loc = 'lower left', fontsize = 12)
# ax3.legend(loc = 'lower')


ax0[0].tick_params(labelsize = 12)
ax0[1].tick_params(labelsize = 12)
# ax1.tick_params(labelsize = 18)
# ax2.tick_params(labelleft = False, labelbottom = False, labelsize = 18)
ax1[0].tick_params(labelsize = 12)
ax1[1].tick_params(labelsize = 12)
# ax.yaxis.offsetText.set_fontsize(12)
ax0[1].legend(loc = 'lower left', fontsize = 14)
ax1[1].legend(loc = 'lower left', fontsize = 14)
ax1[0].legend(loc = 'lower left', ncols = 2)
ax0[0].set_xlabel(r'$|\omega^e/\omega^e_{rms}|$', size = 15)
ax0[1].set_xlabel(r'$|\omega^e/\omega^e_{rms}|$', size = 15)
ax1[0].set_xlabel(r'$|j/j_{rms}|$', size = 15)
ax1[1].set_xlabel(r'$|j/j_{rms}|$', size = 15)
ax1[0].set_xlim(0, 4)
ax0[0].set_xlim(0, 3)
ax1[0].set_ylim(1.1 * 10**(-3),1.1)
# ax0[0].set_ylim(8 * 10**(-6), 1.5)
# fig5.supxlabel(r'$|j/j_{rms}|$', size = 20)
fig5.savefig(figs + 'Fn2.png', dpi = 200)
# fig.clf()