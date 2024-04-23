import numpy as np
import numpy.fft as nf

def EnSpec2D(dbx, dby, dbz, kf = np.inf, numbins = 1, lx = 2 * np.pi, ly = 2 * np.pi):
    '''
    Calculation of omnidirectional magnetic/velocity energy spectrum using

    input: 
    dbx: np.array(floats); dbx = Bx(t) - <Bx(t)>  
    dby: np.array(floats); dby = By(t) - <By(t)>
    kf: float; value to filter energy spectrum
    numbins:int; number of bins to sum for each value k
    lx:float; size of box in x
    ly:float; size of box in y

    output:
    kbins: np.array(floats); binning of k values between kmin and kmax by numbins
    En : np.array(floats); dbx(k) + dby(k) summed between k + dk in kbins
    '''
    nx = dbx.shape[0]
    ny = dbx.shape[1]

    fdbx = np.fft.fftshift(np.fft.fftn(dbx))/(nx * ny)
    fdbx = np.abs(fdbx)**2/2
    fdbx = fdbx.flatten()

    fdby = np.fft.fftshift(np.fft.fftn(dby))/(nx * ny)
    fdby = np.abs(fdby)**2/2
    fdby = fdby.flatten()

    fdbz = np.fft.fftshift(np.fft.fftn(dbz))/(nx * ny)
    fdbz = np.abs(fdbz)**2/2
    fdbz = fdbz.flatten()

    kfreqx = nf.fftshift(nf.fftfreq(nx))* 2 * np.pi * (nx/lx)
    kfreqy = nf.fftshift(nf.fftfreq(ny))* 2 * np.pi * (ny/ly)
    kfreq2D = np.meshgrid(kfreqx, kfreqy) 
    knrm = np.sqrt(kfreq2D[0]**2 + kfreq2D[1]**2)
    knrm = knrm.flatten()

    sort_ind = np.argsort(knrm)
    knrm_sort = knrm[sort_ind]
    fdbx_sort = fdbx[sort_ind]
    fdby_sort = fdby[sort_ind]
    fdbz_sort = fdbz[sort_ind]
    kmin = np.sqrt((2 * np.pi/lx)**2 + (2 * np.pi/ly)**2)
    print(knrm_sort[0])
    print(knrm_sort[-1])
    kbins = np.linspace(kmin, knrm_sort[-1], numbins)
    fdbx_sum = np.zeros(len(kbins))
    fdby_sum = np.zeros(len(kbins))
    fdbz_sum = np.zeros(len(kbins))
    k_len = int(len(knrm_sort))
    kbin_len = int(len(kbins))
    iter = int(k_len/kbin_len)
    for i in np.arange(0,len(kbins)):
        if kbins[i] < kf:
            fdbx_sum[i] =np.sum(fdbx_sort[i * iter: (i+1)*iter])
            fdby_sum[i] =np.sum(fdby_sort[i * iter: (i+1)*iter])
            fdbz_sum[i] =np.sum(fdbz_sort[i * iter: (i+1)*iter])
        else :
            fdbx_sum[i] = 0
            fdby_sum[i] = 0
            fdbz_sum[i] = 0
    En = fdbx_sum + fdby_sum 
    # + fdbz_sum
    return kbins,  En

def EbSpec2D(dbx, dby, dbz, lx = 2 * np.pi, ly = 2 * np.pi):
    nx = dbx.shape[0]
    ny = dbx.shape[1]
    
    fdbx = np.fft.fftshift(np.fft.fftn(dbx))/(nx * ny)
    fdbx = np.abs(fdbx)**2/2
    fdbx = fdbx.flatten()
    
    fdby = np.fft.fftshift(np.fft.fftn(dby))/(nx * ny)
    fdby = np.abs(fdby)**2/2
    fdby = fdbx.flatten()

    fdbz = np.fft.fftshift(np.fft.fftn(dbz))/(nx * ny)
    fdbz = np.abs(fdbz)**2/2
    fdbz = fdbx.flatten()

    kfreqx = np.fft.fftshift(np.fft.fftfreq(nx) * nx * 2 * np.pi/ lx)
    kfreqy = np.fft.fftshift(np.fft.fftfreq(ny) * ny * 2 * np.pi/ ly)
    kfreq2D = np.meshgrid(kfreqx, kfreqy)
    knrm = np.sqrt(kfreq2D[0]**2 + kfreq2D[1]**2)
    knrm = knrm.flatten()
    
    kbins = np.linspace(int(np.min(knrm)), int(np.max(knrm)), 10 * int(np.max(knrm)))
    fdbx_av = np.zeros(len(kbins))
    fdby_av = np.zeros(len(kbins))
    fdbz_av = np.zeros(len(kbins))
    for k in np.arange(0,len(kbins)-1):
        index = np.where((knrm > kbins[k]) & (knrm <= kbins[k+1]))[0]
        if (len(index) == 0):
            fdbx_av[k] = 0
            fdby_av[k] = 0
            fdbz_av[k] = 0
        else:
            # print(fdbx[index])
            fdbx_in = fdbx[index]
            fdby_in = fdby[index]
            fdbz_in = fdby[index]
            # print(fdbx_in)
            fdbx_av[k] = np.sum(fdbx_in)
            fdby_av[k] = np.sum(fdby_in)
            fdbz_av[k] = np.sum(fdbz_in)
        fdb_av = fdbx_av + fdby_av + fdbz_av
    return kbins, fdb_av