from .vpic_info import *
from .load_vars import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def make_movie(dirs, deck, var= 'jz', interval = 100, min = 0.0, max = 0.1, saveas = 'var', fl = 'mp4', lab = 'var', figshape = (10, 10), cmap = 'seismic'):
   vars = load_var('jz', dirs, 0, 'electron')
   figs = '/pscratch/sd/g/goodwill/Fig/' + deck

   vpic_info = get_vpic_info(dirs)
   times = get_times(dirs)
   dt = vpic_info['dt*wci']
   Lx = np.linspace(0, vpic_info['Lx/di'], int(vpic_info['nx']))
   Ly = np.linspace(0,vpic_info['Ly/di'], int(vpic_info['ny']))
   
   fig, ax = plt.subplots(figsize=figshape)
   cax = ax.pcolormesh(Ly, Lx, np.array(vars), cmap = cmap, vmin = min, vmax = max)
   ax.set_xlabel(r'$Y (d_i)$')
   ax.set_ylabel(r'$X (d_i)$')
   fig.colorbar(cax, label = lab)
   def animate(i):
      if i % 10 == 0 :
         print(times[i])
      vars = load_var('jz', dirs, times[i], 'electron')
      ax.set_title(r'$(t \omega_{ci} =$' + str(np.round(times[i] * dt,2)) + ')')
      cax.set_array(np.array(vars).flatten())
      return cax

   anim = animation.FuncAnimation(fig, animate , interval = interval, frames=len(times) - 2)
   anim.save(figs + saveas + '.' + fl)
   plt.show()
