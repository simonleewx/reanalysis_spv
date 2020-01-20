import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from netCDF4 import Dataset,num2date
from matplotlib.ticker import ScalarFormatter

def plot_nam(year,month,day,lag1,lag2):
	"""
	Plots NAM cross section for central date of 'date' and
	lag of 'lag' either side.
	"""
	date = datetime(year,month,day)
	f = Dataset("nam_era5.nc",mode='r')
	time = num2date(f.variables['time'][:],f.variables['time'].units,\
	f.variables['time'].calendar)
	levs = f.variables['level'][:]

	# Extract just the required data to plot
	time_idx = np.where(time==date)[0][0]
	time_plot = time[time_idx-lag1:time_idx+lag2+1]
	nam_plot = f.variables['pc'][:][time_idx-lag1:time_idx+lag2+1]

	f.close()

	clevs = np.arange(-4,4.5,0.5) # filled contour levels
	cr_levs = np.concatenate((np.arange(-10,0,1),np.arange(1,11,1))) # contour line levels, not including 0
	nlevs = len(clevs)-1
	cmap = plt.get_cmap(name='RdBu',lut=nlevs)

	fig = plt.figure(figsize=(10,5))
	ax = fig.add_subplot(111)
	cf = plt.contourf(time_plot,levs,nam_plot.transpose(),levels=clevs,cmap=cmap,extend='both')
	cr = plt.contour(time_plot,levs,nam_plot.transpose(),levels=cr_levs,colors='k',extend='both')
	plt.clabel(cr,inline=1,fmt='%d')
	cmap._lut[int(nlevs/2)-1:int(nlevs/2)+1] = [1.,1.,1.,1.] # make centre of colorbar white
	cb = plt.colorbar(cf,drawedges=True)
	cb.set_label("Standardised departure ($\sigma$)")
	plt.ylabel("Pressure (hPa)")
	plt.semilogy(subsy=[1000,700,500,300,200,100,70,30,10,5,1])
	ax.yaxis.set_major_formatter(ScalarFormatter()) 
	ax.yaxis.set_minor_formatter(ScalarFormatter())
	plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
	plt.axvline(x=date,linestyle='--',color='k') ## vertical line on central date
	plt.gca().invert_yaxis()
	plt.title("ERA-5 Northern Annular Mode (NAM)",loc='left')
	return fig, nam_plot

fig,nam_plot = plot_nam(1998,12,15,15,120)
fig.show()
