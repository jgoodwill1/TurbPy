from .vpic_info import *
from .load_vars import *
from .kfilter import *
import h5py


def hydro_filter(dirs, sp = 'electron', kf = np.inf, lx = 2 * np.pi, ly = 2* np.pi):
    path = dirs + 'filter_hdf5/'
    times = get_times(dirs)
    for i in np.arange(len(times)):
        t = times[i]
        if i % 10 == 0:
            print(t)
        dse = load_vars(dirs, t, species = sp)
        jx = kfilter(dse['jx'],   kf, lx = lx, ly = ly)
        jy = kfilter(dse['jy'],   kf, lx = lx, ly = ly)
        jz = kfilter(dse['jz'],   kf, lx = lx, ly = ly)
        px = kfilter(dse['px'],   kf, lx = lx, ly = ly)
        py = kfilter(dse['py'],   kf, lx = lx, ly = ly)
        pz = kfilter(dse['pz'],   kf, lx = lx, ly = ly)
        txx = kfilter(dse['txx'], kf, lx = lx, ly = ly)
        tyy = kfilter(dse['tyy'], kf, lx = lx, ly = ly)
        tzz = kfilter(dse['tzz'], kf, lx = lx, ly = ly)
        txy = kfilter(dse['txy'], kf, lx = lx, ly = ly)
        tzx = kfilter(dse['tzx'], kf, lx = lx, ly = ly)
        tyz = kfilter(dse['tyz'], kf, lx = lx, ly = ly)
        rho = kfilter(dse['rho'], kf, lx = lx, ly = ly)
        try:  
            os.mkdir(path + f'T.{t}/')  
        except OSError as error:  
            print(error)
        e = h5py.File(path + f'T.{t}/' + f'{sp}_{t}.h5', 'w')
        # print(cbx)
        e.create_dataset("jx", data = jx)
        e.create_dataset("jy", data = jy)
        e.create_dataset("jz", data = jz)
        e.create_dataset("px", data = px)
        e.create_dataset("py", data = py)
        e.create_dataset("pz", data = pz)
        e.create_dataset("txx", data = txx)
        e.create_dataset("tyy", data = tyy)
        e.create_dataset("tzz", data = tzz)
        e.create_dataset("txy", data = txy)
        e.create_dataset("tzx", data = tzx)
        e.create_dataset("tyz", data = tyz)
        e.create_dataset("rho", data = rho)
        e.close()

def field_filter(dirs, kf = np.inf, lx = 2 * np.pi, ly = 2 * np.pi):
    path = dirs + 'filter_hdf5/'
    times = get_times(dirs)
    for i in np.arange(len(times)):
        t = times[i]
        dse = load_vars(dirs, t, species = 'electron')
        cbx = kfilter(dse['cbx'], kf, lx = lx, ly = ly)
        cby = kfilter(dse['cby'], kf, lx = lx, ly = ly)
        cbz = kfilter(dse['cbz'], kf, lx = lx, ly = ly)
        ex = kfilter(dse['ex'],   kf, lx = lx, ly = ly)
        ey = kfilter(dse['ey'],   kf, lx = lx, ly = ly)
        ez = kfilter(dse['ez'],   kf, lx = lx, ly = ly)
        try:  
            os.mkdir(path + f'T.{t}/')  
        except OSError as error:  
            print(error)
        f = h5py.File(path + f'T.{t}/' + f'fields_{t}.h5', 'w')
        # print(cbx)
        f.create_dataset("cbx", data = cbx)
        f.create_dataset("cby", data = cby)
        f.create_dataset("cbz", data = cbz)
        f.create_dataset("ex", data = ex)
        f.create_dataset("ey", data = ey)
        f.create_dataset("ez", data = ez)
        f.close()