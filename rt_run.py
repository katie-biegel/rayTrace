#!/usr/bin/env python
import numpy as np
import os
import sys
import rt_functions as rt
import time

"""
Script runs rayTrace from hypoDD (v1.3)
rayTrace is the raytracing component of the hypoDD software package translated by K. Biegel
And includes python functions for the following subroutines from hypodd:
	direct1.f 	--->  	rt.direct()    	# Traveltime for direct upward-departing wave
 	vmodel.f  	--->	rt.vmodel()		# Extract's needed information from velocity model
 	tiddid.f 	--->	rt.tidddid()	# Determines traveltime intercept and critical 
										  distance in a layered model
	delaz2.f 	--->	rt.delaz()		# Computes distance and azimuth on a sphere
	refract.f 	--->	rt.refract()	# Finds refracted ray with smallest traveltime
	ttime.f 	--->	rt.ttime()		# Determines fastest traveltime between source 
										  and receiver
	partials.f 	--->	rt.partials()	# Returns traveltimes and partial time derivatives
										  for all source/receiver pairs

Note README file for all necessary citations for use of this program package.

To run this script there are two required inputs.
	1. the input file location string (default='rayTrace.inp')
	2. the output file location string (default='rayTrace.src')
Examples of these can be found in the example/ folder or in the README

Examples of all data files required to run this package (event.dat and station.dat) 
can also be found in the example/ folder or in the README.  This format is consistent
with hypoDD and therefore can be run on both software packages.

rayTrace outputs a source file (default='raytrace.src').
This file is free format where each row includes:
	Event ID	P Traveltime (s) 	S Traveltime (s)	Station ID 	  Distance (km)		Azimuth (Deg) 	Takeoff Angle (Deg)
The output file is written in the partials function.ex
"""

def readinputfile(fileloc='rayTrace.inp'):
	"""
	This function read the input file for rayTrace.
	###########
	PARAMETERS:
	fileloc (str) ---- Input file location (default='raytrace.inp')
	############
	RETURNS:
	eventfile (str) ---- Event file location
	statfile (str) ---- Station file location
	mod_nl (int) ---- Number of velocity model layers
	mod_ratio (float) ---- VPVS ratio
	mod_top	(float array) ---- Depth to top of layers (km)
	mod_v (float array) ---- P velocity of layers (km)
	###########
	"""
	inputfile = open(fileloc)
	inputs = inputfile.readlines()
	l = 0
	for line in inputs:
		line = line.split()
		line = list(filter(None,line))
		if line[0] == '*':
			continue
		else:
			if l == 0:
				statfile = str(line[0])
			elif l == 1:
				eventfile = str(line[0])
			elif l == 2:
				mod_nl = int(line[0])
			elif l == 3:
				mod_ratio = float(line[0])
			elif l == 4:
				mod_top = np.asarray(line,dtype=np.float32)
			elif l == 5:
				mod_v = np.asarray(line,dtype=np.float32)
			l = l+1

	return eventfile,statfile,mod_nl,mod_ratio,mod_top,mod_v


def readevents(fileloc):
	"""
	This function reads the event.dat file into numpy arrays
	###########
	PARAMETERS:
	fileloc (str) ---- Event.dat file location
	###########
	RETURNS:
	nsrc (int) ---- Number of events/sources
	src_cusp (int array) ---- Event IDS (integer number labels; must be unique)
	src_lat (float array) ---- Event latitudes
	src_lon (float array) ---- Event longitudes
	src_dep (float array) ---- Event depths
	###########
	"""
	# Read file
	eventfile = open(fileloc,'r')
	events = eventfile.readlines()
	# Initialize arrays
	nsrc = len(events)
	src_cusp = np.zeros(nsrc)
	src_lat = np.zeros(nsrc)
	src_lon = np.zeros(nsrc)
	src_dep = np.zeros(nsrc)
	# Fill arrays
	for index,event in enumerate(events):
		event = event.split()
		event = list(filter(None,event))
		src_cusp[index] = event[-1]
		src_lat[index] = event[2]
		src_lon[index] = event[3]
		src_dep[index] = event[4]

	return nsrc,src_cusp,src_lat,src_lon,src_dep


def readstats(fileloc):
	"""
	This function reads the event.dat file into numpy arrays
	###########
	PARAMETERS:
	fileloc (str) ---- Station.dat file location
	###########
	RETURNS:
	nsta (int) ---- Number of stations
	sta_lab (str array) ---- Station names (must be unique)
	sta_lat (float array) ---- Station latitudes
	sta_lon (float array) ---- Station longitudes
	###########
	"""
	# Read file
	statfile = open(fileloc,'r')
	stats = statfile.readlines()
	# Initialize arrays
	nsta = len(stats)
	sta_lab = np.empty(nsta,dtype='object')
	sta_lat = np.zeros(nsta)
	sta_lon = np.zeros(nsta)
	# Fill arrays
	for index,stat in enumerate(stats):
		stat = stat.split(' ')
		stat = list(filter(None,stat))
		sta_lab[index] = stat[0]
		sta_lat[index] = float(stat[1])
		sta_lon[index] = float(stat[2])

	return nsta,sta_lab,sta_lat,sta_lon




# RUN FROM INPUT TO OUTPUT
try:
	#import pdb;pdb.set_trace()
	inputs = sys.argv
except:
	print('User Enter Inputs:')
	inputfile = input('Inputfile location.  Default = "rayTrace.inp"')
	if not inputfile:
		inputfile = 'rayTrace.inp'
	outputfile = input('Outputfile location.  Default = "rayTrace.src"')
	if not outputfile:
		outputfile = 'rayTrace.src'

if len(inputs) ==1:
	print('User Enter Inputs:')
	inputfile = input('Inputfile location.  Default = "rayTrace.inp"')
	if not inputfile:
		inputfile = 'rayTrace.inp'
	outputfile = input('Outputfile location.  Default = "rayTrace.src"')
	if not outputfile:
		outputfile = 'rayTrace.src'
elif len(inputs) > 1 and len(inputs) < 3:
	raise RuntimeError('Not enough inputs.  Run format: run rt_run.py [inputfile] [outputfile]') 
elif len(inputs) == 3:
	inputfile = inputs[1]
	outputfile = inputs[2]
else:
	raise RuntimeError('Inputs file issues. Run format: run rt_run.py [inputfile] [outputfile]')


# Initialise data
eventfile,statfile,mod_nl,mod_ratio,mod_top,mod_v = readinputfile(inputfile)
nsrc,src_cusp,src_lat,src_lon,src_dep = readevents(eventfile)
nsta,sta_lab,sta_lat,sta_lon = readstats(statfile)

start = time.time()
print('Starting Partials')
tmp_ttp,tmp_tts,tmp_xp,tmp_yp,tmp_zp = rt.partials(nsrc,src_cusp,src_lat,src_lon,src_dep,nsta,sta_lab,sta_lat,
												   sta_lon,mod_nl,mod_ratio,mod_v,mod_top,outputfile)
end = time.time()
print('rayTrace complete.  Outputs located in %s.  Time elapsed %f' % (outputfile,end-start))

