#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
import os, sys
import re
import glob, shutil
import numpy as np

import miriad as mir

## Get list of files #
 #
 # params str   dirpath   Path to directory
 #
 # return list files
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def get_items(dirpath, ext=''):
	if( len(ext) == 0 ):
		files = glob.glob(dirpath + '*')
	else:
		files = glob.glob(dirpath + '*.' + ext)
	
	for i,x in enumerate(files):
		x        = x.replace(dirpath, '')
		if( len(ext) > 0 ):
			x    = x.replace('.' + ext, '')
		files[i] = x

	files.sort()
	return files










## get content from a file
 #
 # params str fname   File name
 #
 # return str txt     content of the file
 # 
 # Version 1/2020
 # Author Hiep Nguyen
 ##
def get_content(fname, project, full=False):
	if(full):
		fpath = 'cmd/full/'+fname
	else:
		fpath = 'cmd/recommend/'+fname

	with open(fpath, 'r') as f:
		txt = f.read()
		txt = txt.strip()

	if(fname == 'atlod'):
		datfiles = get_items( 'projects/'+project+'/data/', ext='' )
		fstr = ''
		if( len(datfiles) == 1 ):
			fstr = 'projects/'+project+'/data/' + datfiles[0]

		if( len(datfiles) > 1 ):
			ext = datfiles[0].split('.')
			ext = ext[-1]
			fstr = 'projects/'+project+'/data/*.'+ext

		if( txt[:3] == 'in='):
			txt = txt.replace('in=', 'in='+fstr )

		txt = txt.replace('out=', 'out='+'projects/'+project+'/'+project+'.uv' )

	else:
		if( txt[:3] == 'in='):
			txt = txt.replace('in=', 'in='+'projects/'+project+'/' )

		txt = txt.replace('out=', 'out='+'projects/'+project+'/' )
		txt = txt.replace('vis=', 'vis='+'projects/'+project+'/' )

	return txt



## Validate the kwargs
 #
 # params str kwargs   kwargs
 #
 # return str kwargs   kwargs
 # 
 # Version 1/2020
 # Author Hiep Nguyen
 ##
def valid_args( **kwargs ):
	delk = []
	for k,v in kwargs.items():
		if( len(v) == 0 ):
			delk.append( k )

	for k in delk:
		del kwargs[k]

	return kwargs


## get arguments of a command
 #
 # params str fname   command
 #
 # return str txt     content of the file
 # 
 # Version 1/2020
 # Author Hiep Nguyen
 ##
def get_args( cmd, txt ):
	txt = txt.strip()

	if( len(txt) == 0 ):
		print('Please add arguments!')
		return None

	txt = txt.replace('\'','')
	txt = txt.replace('\"','')
	txt = txt.replace('\n',';')

	if( txt[:3] == 'in='):
		txt = txt.replace('in=','_in=')

	kwargs = dict(z.split('=') for z in txt.split(';'))
	kwargs = valid_args( **kwargs )
	
	return kwargs



## get arguments of a command
 #
 # params str fname   command
 #
 # return str txt     content of the file
 # 
 # Version 1/2020
 # Author Hiep Nguyen
 ##
def _exe(prj, cmd, kwargs):
	try:
		s = getattr(mir, cmd)( **kwargs )
	except Exception as e:
		s = e
		print('Error! \n')



	# if(cmd == 'uvsplit'):
	# 	try:
	# 		s = mir.uvsplit( **kwargs )
	# 		s = s.decode('utf-8'); print(s)

	# 		dirs = glob.glob('./*/')
	# 		dirs = glob.glob('*.[0-9][0-9][0-9][0-9]*', recursive=False) # 1 dot and 4 digits: '.[0-9][0-9][0-9][0-9]'

	# 		freqlist = []
	# 		for d in dirs:
	# 			spl = d.split('.')
	# 			freqlist.append( spl[1] )
	# 		freqlist = set(freqlist)

	# 		for freq in freqlist:
	# 			frpath = 'projects/'+prj+'/'+freq
	# 			if os.path.exists( frpath ):
	# 			    shutil.rmtree( frpath )
	# 			if not os.path.exists(freq):
	# 			    os.mkdir(freq)

	# 		for d in dirs:
	# 			spl = d.split('.')
	# 			shutil.move(d, spl[1])

	# 		# shutil.rmtree( kwargs['vis'] ) # Remove the oupu file

	# 		for d in freqlist:
	# 			shutil.move( d, 'projects/'+prj+'/' )

	# 		print('Finish - '+ cmd + ' !')
	# 		print('Next: Look at data using "uvplt", "uvspec"')
	# 		print('Then: uvflag -> mfcal')
	# 		print('------')
	# 		print()
	# 	except Exception as e:
	# 		s = e
	# 		print('Error! \n')

	return s