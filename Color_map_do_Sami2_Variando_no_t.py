# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from array import array
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp2d
#from scipy.interpolate import RectBivariateSpline

arr=[]
file=open('denif.dat','r')
#read line into array 
for lines in file.readlines():
    # add a new sublist
    arr.append([])
    # loop over the elemets, split by whitespace
    for i in lines.split():
        # convert to integer and append to the last
        # element of the list
        arr[-1].append(float(i))
# arr é da classe lista
# print('arr=',arr)

#Dimensão de arr: a(linha), b(coluna)
a,b=np.shape(arr)

#Transformando a variavel arr(lista) em array
neoarr=np.zeros(shape=(a,b))
neoarr=np.asarray(arr)

comp=a*b
dat=np.zeros(shape=(comp))

#Criação dos dat's
for i in range (0,a):
    for j in range (0,b):
            dat[b*(i)+j] = neoarr[i,j]

print('linha =',a,'coluna',b)
print('Comprimento de arr',len(dat))
#Criar o Array lendo a partir dos parametros ni,nf,nz,nt

nz = 201
nf = 120
ni = 7
nt = 94

dados=np.zeros(shape=(nz,nf,ni,nt))
glat=np.zeros(shape=(nz,nf))
zalt=np.zeros(shape=(nz,nf))

#Leitura da LDesidade das espécies
for l in range (0,nt):
    for k in range (0,ni):
        for j in range (0,nf):
            for i in range (0,nz):
                dados[i,j,k,l]=dat[(l)*nz*nf*ni+(k)*nz*nf+(j)*nz+i]
                
#Leitura da altitude e da latitude
arr1=[]
file1=open('glatf.dat','r')
#read line into array 
for lines in file1.readlines():
    # add a new sublist
    arr1.append([])
    # loop over the elemets, split by whitespace
    for i in lines.split():
        # convert to integer and append to the last
        # element of the list
        arr1[-1].append(float(i))

#arr é da classe lista
#print('arr=',arr)


#Dimensão de arr: a(linha), b(coluna)
a,b=np.shape(arr1)

#Transformando a variavel arr(lista) em array
neoarr1=np.zeros(shape=(a,b))
neoarr1=np.asarray(arr1)

comp=a*b

#Vamos preencher o vetor neoarr com dimensão(a,b) em um vetor coluna(1,comp)
dat1=np.zeros(shape=(comp))

#Vamos preencher o vetor neoarr1 com dimensão(a,b) em um vetor coluna(1,comp)
dat2=np.zeros(shape=(comp))

for i in range (0,a):
    for j in range (0,b):
            dat1[b*(i)+j] = neoarr1[i,j]      

arr2=[]
file2=open('zaltf.dat','r')
#read line into array 
for lines in file2.readlines():
    # add a new sublist
    arr2.append([])
    # loop over the elemets, split by whitespace
    for i in lines.split():
        # convert to integer and append to the last
        # element of the list
        arr2[-1].append(float(i))

#arr é da classe lista
#print('arr=',arr)

#Dimensão de arr: a(linha), b(coluna)
a,b=np.shape(arr2)

#Transformando a variavel arr(lista) em array
neoarr2=np.zeros(shape=(a,b))
neoarr2=np.asarray(arr2)
dados1 = np.zeros(shape=nz)
dados2 = np.zeros(shape=nf)

comp=a*b

#Vamos preencher o vetor neoarr2 com dimensão(a,b) em um vetor coluna(1,comp)
for i in range (0,a):
    for j in range (0,b):
            dat2[b*(i)+j] = neoarr2[i,j]            

#Leitura da Latitude
for j in range (0,nf):
    for i in range (0,nz):
        glat[i,j]=dat1[(j)*nz+i]                                

#Leitura da Altitude
for j in range (0,nf):
    for i in range (0,nz):
        zalt[i,j]=dat2[(j)*nz+i]                

# definições para a plotagem dos mapas
lat_min = -40.0
lat_max = 25.0
alt_min = 100.0
alt_max = 800.0

len_lat = 80
len_alt = 80


lat=glat[0:nz,60]
alt_lat = zalt[100,60]
alt=zalt[100,0:nf]
lat_alt = glat[100,0]

for tt in range (0, nt, 1):

  # Plota seção em altitude fixa e latitude fixa
  # for i in range (0,ni):
  #   dados1= dados1 + dados[0:nz,60,i,1] #31, default
  # for i in range (0,ni):
  #  dados2= dados2 + dados[100,0:nf,i,1] #31, default
  #print('Grafico de altitude -> Latitude da base fixa em =', lat_alt )
  #print('Grafico de latitude -> Altitude maxima (equador magnetico) =', alt_lat )

  #plt.figure(1)
  #plt.plot(lat, dados1)
  #plt.ylabel('densidade')
  #plt.xlabel('Latitude')

  #plt.figure(2)
  #plt.plot(dados2,alt)
  #plt.xlabel('densidade')
  #plt.ylabel('Altitude')

  d_lat_max = np.mean(abs(np.diff(lat)))
  lat_range = max(lat) - min(lat)
  d_alt_max = np.mean(abs(np.diff(alt)))
  alt_range = max(alt) - min(alt)


  #print('D_lat_mean = ', d_lat_max, 'D_alt_mean = ',  d_alt_max)
  
  R2 = (d_lat_max/lat_range)**2 + (d_alt_max/alt_range)**2
  print('R2 = ', R2)
  print('Time index =', tt)

  X = np.linspace(lat_min, lat_max,len_lat)
  Y = np.linspace(alt_min, alt_max, len_alt)
  x, y = np.meshgrid(X, Y)

  z = np.zeros((len_lat, len_alt))

  flag = 0

  for i in range (0,len_lat):
     for j in range (0,len_alt):
       for jj in range (0,nf):
         for ii in range (0,nz):  
           diff_alt = y[i,j] - zalt[ii,jj]
           diff_lat = x[i,j] - glat[ii,jj] 
           if np.logical_and((diff_alt/alt_range)**2 + (diff_lat/lat_range)**2  <= R2, diff_lat <= d_lat_max): 
             ii_sol = ii
             jj_sol = jj
             R2 = (diff_lat/lat_range)**2 + (diff_alt/alt_range)**2
             flag = 1
       if flag == 1:
         for l in range (0,ni):
           z[i,j] = z[i,j] + dados[ii_sol,jj_sol,l,tt] #31, default
         R2 = (d_lat_max/lat_range)**2 + (d_alt_max/alt_range)**2
         flag = 0
       else: 
         z[i,j] = 0.0

  # x and y are bounds, so z should be the value *inside* those bounds.
  # Therefore, remove the last value from the z array.
  z_plot = z[:-1, :-1]
  #levels = MaxNLocator(nbins=30).tick_values(z.min(), z.max())


  # pick the desired colormap, sensible levels, and define a normalization
  # instance which takes data values and translates those into levels.
  cmap = plt.get_cmap('hot')
  #bounds=[0,100000,200000,300000,400000,500000,600000,700000,800000]
  #norm = mpl.colors.Normalize(vmin=0, vmax=800000) # linear map
  bounds=[100,1000,10000,100000,1000000, 10000000] 
  norm = mpl.colors.LogNorm(vmin=100, vmax=10000000) # log map
  fig1, (ax1) = plt.subplots(nrows=1)
  im = ax1.imshow(z_plot, cmap=cmap, norm=norm, aspect = 'auto' , interpolation='gaussian', origin='lower', extent = [lat_min, lat_max, alt_min, alt_max])
  fig1.colorbar(im, ax=ax1, norm=norm, ticks=bounds)
  ax1.set_title('imshow with levels')
  name_fig = 'density_map' + str(tt) + '.png'
  plt.savefig(name_fig, bbox_inches='tight')
  #im = ax1.pcolormesh(x,y,z, cmap=cmap, norm=norm)
  #fig1.colorbar(im, ax=ax1)
  #ax1.set_title('pcolormesh with levels')

  ## scipy interp. cubic
  #f = interp2d(X, Y, z, kind='linear')
  ##f = RectBivariateSpline(X, Y, z)
  #xnew = np.arange(lat_min, lat_max, .1)
  #ynew = np.arange(alt_min, alt_max, 1)
  #znew = f(xnew,ynew)
  #Xn, Yn = np.meshgrid(xnew, ynew)
  #fig2, (ax2) = plt.subplots(nrows=1)
  #im = ax2.pcolormesh(Xn, Yn, znew, cmap='hot')
  #fig2.colorbar(im, ax=ax2)
  #ax2.set_title('cubic interpolation')

  plt.draw()

#plt.show()
