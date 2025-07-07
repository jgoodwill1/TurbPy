from .vpic_info import *
from .load_vars import *
from .kfilter import *
from .vorticity import *
from .JE_calc import *
from .ps_calc import *
from ..imports import *


deck = 'KH_200ppc_200wci/'
dirs = '/pscratch/sd/g/goodwill/' + deck
figs = '/pscratch/sd/g/goodwill/Fig/' + deck
info = get_vpic_info(dirs)
times = get_times(dirs)
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

def Fn(t, min, max, jfilt = True, wfilt = False)
  print(twci[t])
  el = load_hydro_fil(dirs, times[t], 'electron')
  ion = load_hydro_fil(dirs, times[t], 'ion')

  if wfilt == True:
    wV = w_calc(dirs, t, sp = 'electron')
    w = np.sqrt(wV[0]**2 + wV[1]**2 + wV[2]**2)
    j = w
  if jfilt == True:
    j = np.sqrt((el['jx'] + ion['jx'])**2 + (el['jy'] + ion['jy'])**2 + (el['jz'] + ion['jz'])**2)

  jrms = np.sqrt(np.mean(j**2))
  jnrm = (j/jrms)[100:1180,:]

  df = pd.DataFrame()
  jmask = np.linspace(min, max, 50)
  JiE, JeE, JE = JE_calc(dirs, times[t])
  JiE = JiE[100:1180,:]
  JeE = JeE[100:1180,:]
  JE =  JE[100:1180,:]
  pthe, pide = ps_calc(dirs, times[t], 'electron')
  pthi, pidi = ps_calc(dirs, times[t], 'ion')
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
  return df