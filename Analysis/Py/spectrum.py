def PerpSpectrum(ar,sumax=2,lenx=2*np.pi,leny=2*np.pi,lenz=2*np.pi):
   """
      PerpSpectrum(ar,sumax=2,lenx=2*pi,leny=2*pi,lenz=2*pi)
      ar -> Array to compute the spectrum
      sumax -> Axis of magnetic field direction. Right now only x,y,z = 0,1,2
      lenx,leny,lenz -> System size in x,y,z directions to take into
                        account the anisotropy of system if any

      RETURNS:
      kk -> Wavenumber array
      fekp -> Spectrum of the array
   """
   if len(ar) == 0:
      print('No array provided! Exiting!')
      return
   ar=ar-np.mean(ar)
   nx=np.shape(ar)[0];kx=nf.fftshift(nf.fftfreq(nx))*nx*(2*np.pi/lenx)
   ny=np.shape(ar)[1];ky=nf.fftshift(nf.fftfreq(ny))*ny*(2*np.pi/leny)
 
   far = nf.fftshift(nf.fftn(ar))/(nx*ny); fftea=0.5*np.abs(far)**2
   ffteb = fftea
## DEFINE A TEMPORARY XY PLANE
   if sumax==2:
      nnx=nx; nny=ny
      kkx=kx; kky=ky
## DEFINE THE KPERP VALUES AND CORRESPONDING SPECTRUM
   fekp=np.zeros(min(nnx//2,nny//2))
   kp=np.zeros((nnx,nny))
   for x in range(nnx):
      for y in range(nny):
         kp[x,y]=np.sqrt(kkx[x]**2+kky[y]**2)
   if nnx == 1:
      dk=np.abs(kp[0,1]-kp[0,0])
      kk=kp[0,nny//2:]
   elif nny == 1:
      dk=np.abs(kp[1,0]-kp[0,0])
      kk=kp[nnx//2:,0]
   else:
      dk=np.abs(kp[1,0]-kp[0,0])
      kk=kp[nnx//2,nny//2:]

   for i in range(len(fekp)):
      fekp[i]= np.sum(np.ma.MaskedArray(ffteb, ~((kp[nx//2,i+ny//2]-dk < kp) & (kp < kp[nx//2,i+ny//2]+dk))))

   return kk,fekp/dk