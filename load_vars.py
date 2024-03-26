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
    