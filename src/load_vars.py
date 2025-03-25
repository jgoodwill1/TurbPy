import numpy as np
import h5py

def load_var(var, dirs, time_step, species = 'electron'):
    '''
    Loads singular variable from timestep in hdf5 files
    input:
    var: string; any variables outputted in hdf5 files
    '''
    
    hydro_file = h5py.File(dirs+"hydro_hdf5/T."+str(time_step)+"/hydro_" + species + "_"+str(time_step)+".h5", 'r')
    field_file = h5py.File(dirs+"field_hdf5/T."+str(time_step)+"/fields_" + str(time_step)+".h5", 'r')
    jvec={}
    var_dict = {}
    if var in field_file['Timestep_'+str(time_step)]:
        group = field_file['Timestep_'+str(time_step)]
        dset = group[var]
        jvec[var+str(time_step)] = np.zeros(dset.shape, dtype=dset.dtype)
        dset.read_direct(jvec[var+str(time_step)])
        var_dict[var] = np.array(dset[:,:,0])
    else:
        group=hydro_file['Timestep_'+str(time_step)]
        dset = group[var]
        jvec[var+str(time_step)] = np.zeros(dset.shape, dtype=dset.dtype)
        dset.read_direct(jvec[var+str(time_step)])
        var_dict[var] = np.array(dset[:,:,0])
    return var_dict[var]
    

def load_vars(dirs, time_step, species = 'electron'):
    hydro_file = h5py.File(dirs+"hydro_hdf5/T."+str(time_step)+"/hydro_" + species + "_"+str(time_step)+".h5", 'r')
    field_file = h5py.File(dirs+"field_hdf5/T."+str(time_step)+"/fields_" + str(time_step)+".h5", 'r')
    
    jvec={}
    var_dict = {}
    vars = ['cbx', 'cby', 'cbz', 'ex', 'ey', 'ez']
    group=field_file['Timestep_'+str(time_step)]

    for i in vars:
        dset = group[i]
        jvec[i+str(time_step)] = np.zeros(dset.shape, dtype=dset.dtype)
        dset.read_direct(jvec[i+str(time_step)])
        var_dict[i] = np.array(dset[:,:,0])

    jvec={}
    vars = ['jx', 'jy', 'jz', 'ke', 'px', 'py', 'pz', 
            'rho', 'txx', 'txy', 'tyy', 'tyz', 'tzx', 'tzz']
    group=hydro_file['Timestep_'+str(time_step)]

    for i in vars:
        dset = group[i]
        jvec[i+str(time_step)] = np.zeros(dset.shape, dtype=dset.dtype)
        dset.read_direct(jvec[i+str(time_step)])
        var_dict[i] = np.array(dset[:,:,0])
    return (var_dict)

def load_fields(dirs, time_step):
    field_file = h5py.File(dirs+"field_hdf5/T."+str(time_step)+"/fields_" + str(time_step)+".h5", 'r')
    
    jvec={}
    var_dict = {}
    vars = ['cbx', 'cby', 'cbz', 'ex', 'ey', 'ez']
    group=field_file['Timestep_'+str(time_step)]

    for i in vars:
        dset = group[i]
        jvec[i+str(time_step)] = np.zeros(dset.shape, dtype=dset.dtype)
        dset.read_direct(jvec[i+str(time_step)])
        var_dict[i] = np.array(dset[:,:,0])
    return (var_dict)

def load_hydro(dirs, time_step, species = 'electron'):
    hydro_file = h5py.File(dirs+"hydro_hdf5/T."+str(time_step)+"/hydro_" + species + "_"+str(time_step)+".h5", 'r')
    var_dict = {}
    hydro_vars = ['jx', 'jy', 'jz', 'px', 'py', 'pz', 'txx', 'tyy', 'tzz', 'txy', 'tzx', 'tyz', 'rho']
    for i in hydro_vars:
        dset = hydro_file['Timestep_'f'{time_step}'][i]
        
        var_dict[i] = np.array(dset[:,:,0])
    return (var_dict)

def load_field_fil(dirs, time_step):
    # hydro_file = h5py.File(dirs+"filter_hdf5/T."+str(time_step)+ "/" + species + "_"+str(time_step)+".h5", 'r')
    field_file = h5py.File(dirs+"filter_hdf5/T."+str(time_step)+"/fields_" + str(time_step)+".h5", 'r')
    var_dict = {}
    field_vars = ['cbx', 'cby', 'cbz', 'ex', 'ey', 'ez']
    # hydro_vars = ['jx', 'jy', 'jz', 'px', 'py', 'pz', 'txx', 'tyy', 'tzz', 'txy', 'tzx', 'tyz', 'rho']
    for i in field_vars:
        dset = field_file[i]
        var_dict[i] = np.array(dset[:,:])
    return (var_dict)

def load_hydro_fil(dirs, time_step, species = 'electron'):
    hydro_file = h5py.File(dirs+"filter_hdf5/T."+str(time_step)+ "/" + species + "_"+str(time_step)+".h5", 'r')
    # field_file = h5py.File(dirs+"filter_hdf5/T."+str(time_step)+"/fields_" + str(time_step)+".h5", 'r')
    var_dict = {}
    hydro_vars = ['jx', 'jy', 'jz', 'px', 'py', 'pz', 'txx', 'tyy', 'tzz', 'txy', 'tzx', 'tyz', 'rho']
    for i in hydro_vars:
        dset = hydro_file[i]
        var_dict[i] = np.array(dset[:,:])
    return (var_dict)
    