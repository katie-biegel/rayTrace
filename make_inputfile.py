#!/usr/bin/env python
from pyrocko import cake
import numpy as np
import os
import obspy.geodetics.base as gps
import rt_functions as rt

def makeinputs(input_file,nsrc,nsta,sta_dist,src_distxy,src_distz,nl,vpvs,top,v):
	# Write to Input File
	inputfile = open(input_file,'w')
	inputfile.write('* RayTrac.INP: \n* --- Station File \nstation.dat \n')
	inputfile.write('* \n* --- Event File \nevent.dat \n')
	inputfile.write('* \n* --- Velocity Model: \n* Number of Layers \n%i \n' % nl)
	inputfile.write('* vpvs ratio \n%2.3f \n* Top of Layers (km) \n' % vpvs)
	for i in range(0,nl):
		inputfile.write('%2.3f    ' % top[i])
	inputfile.write('\n* Layer Velocities (km/s) \n')
	for i in range(0,nl):
		inputfile.write('%2.3f    ' % v[i])
	inputfile.close()

	# Write to station file
	sta_lat = sta_dist*np.random.random(nsta)
	sta_lon = sta_dist*np.random.random(nsta)
	statfile = open('station.dat','w')
	for i in range(0,nsta):
		statfile.write('st%i %8.5f %8.5f \n' % (i,sta_lat[i],sta_lon[i]))
	statfile.close()

	# Write to event file
	src_sqr = (sta_dist - src_distxy)/2.
	src_lat = src_distxy*np.random.random(nsrc) + src_sqr
	src_lon = src_distxy*np.random.random(nsrc) + src_sqr
	src_dep = src_distz*np.random.random(nsrc)
	eventfile = open('event.dat','w')
	for i in range(0,nsrc):
		eventfile.write('20200101   00000001 %8.5f %8.5f %8.5f   1.0   0.0   0.0  0.0 %8i \n' % (src_lat[i],src_lon[i],src_dep[i],i+1))
	eventfile.close()

	return

################
# Edit these lines
input_file = '/Users/katie/Desktop/rayTrace/rayTrace.inp'
nsrc = 50
nsta = 20
sta_dist = 12 # Deg
src_distxy = 8 # Deg
src_distz = 100 # km
nl = 5
vpvs = 1.75
top = np.array([0.0,20.,35.,77.5,120.])
v = np.array([5.8,6.5,8.04,8.045,8.05])

makeinputs(input_file,nsrc,nsta,sta_dist,src_distxy,src_distz,nl,vpvs,top,v)
