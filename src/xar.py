from .vpic_info import *
from .load_vars import *
import xarray as xr
def get_xarray(dir, species = None, var = None):
    vpic_info = get_vpic_info(dir)
    time = get_times(dir)
    nx = int(vpic_info['nx'])
    ny = int(vpic_info['ny'])
    x = np.arange(0,nx)
    y = np.arange(0,ny)
    if var == None:
        bx_all = np.zeros((len(time), nx, ny))
        by_all = np.zeros((len(time), nx, ny))
        bz_all = np.zeros((len(time), nx, ny))

        ex_all = np.zeros((len(time), nx, ny))
        ey_all = np.zeros((len(time), nx, ny))
        ez_all = np.zeros((len(time), nx, ny))
        if species == 'electron':
            jxe_all = np.zeros((len(time), nx, ny))
            jye_all = np.zeros((len(time), nx, ny))
            jze_all = np.zeros((len(time), nx, ny))

            rhoe_all = np.zeros((len(time), nx, ny))

            pxxe_all = np.zeros((len(time), nx, ny))
            pyye_all = np.zeros((len(time), nx, ny))
            pzze_all = np.zeros((len(time), nx, ny))
        if species == 'ion':
            jxi_all = np.zeros((len(time), nx, ny))
            jyi_all = np.zeros((len(time), nx, ny))
            jzi_all = np.zeros((len(time), nx, ny))

            rhoi_all = np.zeros((len(time), nx, ny))

            pxxi_all = np.zeros((len(time), nx, ny))
            pyyi_all = np.zeros((len(time), nx, ny))
            pzzi_all = np.zeros((len(time), nx, ny))
        if species == None:
            jxe_all = np.zeros((len(time), nx, ny))
            jye_all = np.zeros((len(time), nx, ny))
            jze_all = np.zeros((len(time), nx, ny))

            rhoe_all = np.zeros((len(time), nx, ny))

            pxxe_all = np.zeros((len(time), nx, ny))
            pyye_all = np.zeros((len(time), nx, ny))
            pzze_all = np.zeros((len(time), nx, ny))
            jxi_all = np.zeros((len(time), nx, ny))
            jyi_all = np.zeros((len(time), nx, ny))
            jzi_all = np.zeros((len(time), nx, ny))

            rhoi_all = np.zeros((len(time), nx, ny))

            pxxi_all = np.zeros((len(time), nx, ny))
            pyyi_all = np.zeros((len(time), nx, ny))
            pzzi_all = np.zeros((len(time), nx, ny))
    else: 
        varload_all = np.zeros((len(time), nx, ny))
    for i in np.arange(len(time)):
        timestep = time[i]
        if var == None:
            ds =load_fields(dir,timestep)
            bx_all[i] = ds['cbx']
            by_all[i] = ds['cby']
            bz_all[i] = ds['cbz']

            ex_all[i] = ds['ex']
            ey_all[i] = ds['ey']
            ez_all[i] = ds['ez']
            if species == 'electron':
                dse =load_hydro(dir,timestep, species = 'electron')

                jxe_all[i] = dse['jx']
                jye_all[i] = dse['jy']
                jze_all[i] = dse['jz']
                rhoe_all[i] = dse['rho']
                pxxe_all[i] = dse['txx'] - (dse['jx']/dse['rho']) * dse['px']
                pyye_all[i] = dse['tyy'] - (dse['jy']/dse['rho']) * dse['py']
                pzze_all[i] = dse['tzz'] - (dse['jz']/dse['rho']) * dse['pz']
            if species == 'ion':
                dsi =load_hydro(dir,timestep, species = 'ion')

                jxi_all[i] = dsi['jx']
                jyi_all[i] = dsi['jy']
                jzi_all[i] = dsi['jz']
                rhoi_all[i] = dsi['rho']
                pxxi_all[i] = dsi['txx'] - (dsi['jx']/dsi['rho']) * dsi['px']
                pyyi_all[i] = dsi['tyy'] - (dsi['jy']/dsi['rho']) * dsi['py']
                pzzi_all[i] = dsi['tzz'] - (dsi['jz']/dsi['rho']) * dsi['pz']
            if species == None:
                dse =load_hydro(dir,timestep, species = 'electron')

                jxe_all[i] = dse['jx']
                jye_all[i] = dse['jy']
                jze_all[i] = dse['jz']
                rhoe_all[i] = dse['rho']
                pxxe_all[i] = dse['txx'] - (dse['jx']/dse['rho']) * dse['px']
                pyye_all[i] = dse['tyy'] - (dse['jy']/dse['rho']) * dse['py']
                pzze_all[i] = dse['tzz'] - (dse['jz']/dse['rho']) * dse['pz']
                
                dsi =load_hydro(dir,timestep, species = 'ion')

                jxi_all[i] = dsi['jx']
                jyi_all[i] = dsi['jy']
                jzi_all[i] = dsi['jz']
                rhoi_all[i] = dsi['rho']
                pxxi_all[i] = dsi['txx'] - (dsi['jx']/dsi['rho']) * dsi['px']
                pyyi_all[i] = dsi['tyy'] - (dsi['jy']/dsi['rho']) * dsi['py']
                pzzi_all[i] = dsi['tzz'] - (dsi['jz']/dsi['rho']) * dsi['pz']
        else:
            varload_all[i] = load_var(var, dir, timestep, species)
        if var == None:
            if species == 'electron':
                ds = xr.Dataset(
                    {
                        "bx": (["timestep", "x", "y"], bx_all),
                        "by": (["timestep", "x", "y"], by_all),
                        "bz": (["timestep", "x", "y"], bz_all),
                        "ex": (["timestep", "x", "y"], ex_all),
                        "ey": (["timestep", "x", "y"], ey_all),
                        "ez": (["timestep", "x", "y"], ez_all),
                        "jxe": (["timestep", "x", "y"], jxe_all),
                        "jye": (["timestep", "x", "y"], jye_all),
                        "jze": (["timestep", "x", "y"], jze_all),
                        "rhoe": (["timestep", "x", "y"], rhoe_all),
                        "pxxe": (["timestep", "x", "y"], pxxe_all),
                        "pyye": (["timestep", "x", "y"], pxxe_all),
                        "pzze": (["timestep", "x", "y"], pxxe_all),
                    },
                    coords={
                        "x" : x,
                        "y" : y,
                        "timestep" : time,
                    },
                )
            if species == 'ion':
                ds = xr.Dataset(
                    {
                        "bx": (["timestep", "x", "y"], bx_all),
                        "by": (["timestep", "x", "y"], by_all),
                        "bz": (["timestep", "x", "y"], bz_all),
                        "ex": (["timestep", "x", "y"], ex_all),
                        "ey": (["timestep", "x", "y"], ey_all),
                        "ez": (["timestep", "x", "y"], ez_all),
                        "jxi": (["timestep", "x", "y"], jxi_all),
                        "jyi": (["timestep", "x", "y"], jyi_all),
                        "jzi": (["timestep", "x", "y"], jzi_all),
                        "rhoi": (["timestep", "x", "y"], rhoi_all),
                        "pxxi": (["timestep", "x", "y"], pxxi_all),
                        "pyyi": (["timestep", "x", "y"], pxxi_all),
                        "pzzi": (["timestep", "x", "y"], pxxi_all),
                    },
                    coords={
                        "x" : x,
                        "y" : y,
                        "timestep" : time,
                    },
                )

            if species == None:
                ds = xr.Dataset(
                    {
                        "bx": (["timestep", "x", "y"], bx_all),
                        "by": (["timestep", "x", "y"], by_all),
                        "bz": (["timestep", "x", "y"], bz_all),
                        "ex": (["timestep", "x", "y"], ex_all),
                        "ey": (["timestep", "x", "y"], ey_all),
                        "ez": (["timestep", "x", "y"], ez_all),
                        "jxi": (["timestep", "x", "y"], jxi_all),
                        "jyi": (["timestep", "x", "y"], jyi_all),
                        "jzi": (["timestep", "x", "y"], jzi_all),
                        "rhoi": (["timestep", "x", "y"], rhoi_all),
                        "pxxi": (["timestep", "x", "y"], pxxi_all),
                        "pyyi": (["timestep", "x", "y"], pxxi_all),
                        "pzzi": (["timestep", "x", "y"], pxxi_all),
                        "jxe": (["timestep", "x", "y"], jxe_all),
                        "jye": (["timestep", "x", "y"], jye_all),
                        "jze": (["timestep", "x", "y"], jze_all),
                        "rhoe": (["timestep", "x", "y"], rhoe_all),
                        "pxxe": (["timestep", "x", "y"], pxxe_all),
                        "pyye": (["timestep", "x", "y"], pxxe_all),
                        "pzze": (["timestep", "x", "y"], pxxe_all),
                    },
                    coords={
                        "x" : x,
                        "y" : y,
                        "timestep" : time,
                    },
                )
        else:
            ds = xr.Dataset(
                {
                    var: (["timestep", "x", "y"], varload_all),
                },
                coords={
                    "x" : x,
                    "y" : y,
                    "timestep" : time,
                },
            )
    return ds