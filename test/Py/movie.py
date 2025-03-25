import TurbPy as tb
from TurbPy.imports import *
from vpic_info import *

# deck = 'KH_Lv1di/'
# deck = 'turb2/'
deck = 'turb_vth0.01/'
# deck = 'KH_beta0.1/'

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

def make_movie(dirs, deck, interval = 100, saveas = 'var', fl = 'mp4', lab = 'var', figshape = (10, 10), cmap = 'seismic'):
   figs = '/pscratch/sd/g/goodwill/Fig/' + deck
   


   vpic_info = get_vpic_info(dirs)
   times = get_times(dirs)
   dt = vpic_info['dt*wci']
   Lx = np.linspace(0, vpic_info['Lx/di'], int(vpic_info['nx']))
   Ly = np.linspace(0,vpic_info['Ly/di'], int(vpic_info['ny']))
   

   el = tb.load_hydro_fil(dirs, times[0], species = 'electron')
   ion = tb.load_hydro_fil(dirs, times[0], species = 'ion')
   f = tb.load_field_fil(dirs, times[0])

   ds = tb.pcurl(el['jx']/el['rho'],
                el['jy']/el['rho'], 
                el['jz']/el['rho'], 
                dx = info['dx/de'], 
                dy = info['dy/de'], 
                dz = info['dz/de'])
   ds = ds[2]
   # ds = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
   max = np.max(ds)
   fig, ax = plt.subplots(figsize=figshape)
   cax = ax.pcolormesh(Ly, Lx, ds, cmap = cmap, vmin = -max, vmax = max)
   ax.set_xlabel(r'$Y (d_i)$')
   ax.set_ylabel(r'$X (d_i)$')
   fig.colorbar(cax, label = lab)
   plt.show()
   def animate(i):
      if i % 10 == 0 :
         plt.show()
         print(times[i])
      el = tb.load_hydro_fil(dirs, times[i], species = 'electron')
      # ion = tb.load_hydro_fil(dirs, times[i], species = 'ion')
      # ds = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)
      ds = tb.pcurl(el['jx']/el['rho'],
                el['jy']/el['rho'], 
                el['jz']/el['rho'], 
                dx = info['dx/de'], 
                dy = info['dy/de'], 
                dz = info['dz/de'])
      ds = ds[2]
      ax.set_title(r'$(t \omega_{ci} =$' + str(np.round(times[i] * dt,2)) + ')')
      cax.set_array(np.array(ds).flatten())
      plt.show()
      plt.close()
      return cax

   anim = animation.FuncAnimation(fig, animate , interval = interval, frames=len(times) - 2)
   anim.save(figs + saveas + '.' + fl)
   plt.show()


var = r'$omega_e'
make_movie(dirs, deck = deck, saveas = 'w_e.mp4', lab = var, figshape = (12,6))