import os
import re
import numpy as np

def get_josh_info(dirs):
    """
    Get information of the VPIC simulation
    input:
    dirs: string; place where info file is located
    output:
    vpic_info: dict; returns integer given string
    """
    with open(dirs+'info_josh') as f:
        content = f.readlines()
    f.close()
    vpic_info = {}
    for line in content[1:]:
        if "=" in line:
            line_splits = line.split("=")
        elif ":" in line:
            line_splits = line.split(":")

        tail = line_splits[1].split("\n")
        vpic_info[line_splits[0].strip()] = float(tail[0])
    return vpic_info

def get_vpic_info(dirs):
    """
    Get information of the VPIC simulation
    input:
    dirs: string; place where info file is located
    output:
    vpic_info: dict; returns integer given string
    """
    with open(dirs+'info') as f:
        content = f.readlines()
    f.close()
    vpic_info = {}
    for line in content[1:]:
        if "=" in line:
            line_splits = line.split("=")
        elif ":" in line:
            line_splits = line.split(":")

        tail = line_splits[1].split("\n")
        vpic_info[line_splits[0].strip()] = float(tail[0])
    return vpic_info

def get_times(dirs):
    files = os.listdir(dirs + 'hydro_hdf5')
    if os.path.exists(dirs + 'hydro_hdf5/' + 'hydro-electron.xdmf'):
        files.remove('hydro-electron.xdmf')
    if os.path.exists(dirs + 'hydro_hdf5/' + 'hydro-ion.xdmf'):
        files.remove('hydro-ion.xdmf')
    if os.path.exists(dirs + 'hydro_hdf5/' + '.ipynb_checkpoints'):
        files.remove('.ipynb_checkpoints')
    c=0
    time = [None] * len(files)
    for file in files:
        time[c] = int(re.findall(r'\d+', files[c])[0])
        c = c+1
    time.sort()
    return np.array(time)