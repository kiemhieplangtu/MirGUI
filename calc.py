#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
import os, sys
import re
import glob, shutil
import numpy as np

from mirpy import miriad as mir

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





## Read a config file #
 #
 # params str file   path to file
 #
 # return float rms
 #        1-D array v_fltr filtered vlsr 
 #        1-D array T_fltr filtered Tb 
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def load_config(file):
	key_val_dict = {}
	east_coord   = []
	north_coord  = []
	
    # Compile necessary regular expressions
	spaces         = re.compile('\s+')
	comma_n_spaces = re.compile(',\s+')
	comment        = re.compile('#.*')
	quotes         = re.compile('\'[^\']*\'')
	key_val        = re.compile('^.+=.+')
	cols           = re.compile('^.+,.+')

	# Open the file and scan, line by line
	try:
		dat = open(file, "r")
	except Exception:
		print("Failed to open file '%s'." % file)
		return False
	for line in dat:
		line = line.rstrip("\n\r")
		if not comment.match(line):
			line = comment.sub('', line)           # internal comments 
			line = line.replace("'", '')           # remove quotes
			line = comma_n_spaces.sub(',', line)   # kill ambiguous spaces

			# Capture key=value pairs
			if key_val.match(line):
				keyword, value = line.split('=',1)
				value          = value.strip()              # kill ext whitespace 
				keyword        = keyword.strip()       
				value          = spaces.sub('', value)      # shrink int whitespace
				keyword        = spaces.sub('', keyword)    
				if value       :
					key_val_dict[keyword] = value

			# Capture antenna coordinate entries
			if cols.match(line):
				east, north = line.split(',')
				east_coord.append(east)
				north_coord.append(north)
	dat.close()

	# Number of antennas should be > 2
	if (len(east_coord) < 2) :
		print('Number of antennas should be > 2')
		sys.exit()
		return None


	# From Cormac -> Calculate the antenna coordinates in Earth-centred coordinate frame
	# Technically, we should have terms for the distance from the
	# centre of the Earth, but if the elevation is the same for all
	# antennas, these cancel out when calculating the baseline vectors.
	east_coord   = np.array(east_coord, dtype='f4')
	north_coord  = np.array(north_coord, dtype='f4')
	latitude_deg = float(key_val_dict.get('latitude_deg', 20.0))
	latitude_rad = np.radians(latitude_deg)
	x_m          = -north_coord*np.sin(latitude_rad)
	y_m          = east_coord
	z_m          = north_coord*np.cos(latitude_rad)

	ret = {}
	ret['telescope']     = key_val_dict.get('telescope', 'UNKNOWN')
	ret['config']        = key_val_dict.get('config', 'UNKNOWN')
	ret['latitude_deg']  = latitude_deg
	ret['latitude_rad']  = latitude_rad
	ret['diameter_m']    = float(key_val_dict.get('diameter_m', 22.0))
	ret['east_coord_m']  = east_coord
	ret['north_coord_m'] = north_coord
	ret['n_ant']         = int(len(ret['east_coord_m']))
	ret['n_base']        = int(ret['n_ant']*(ret['n_ant']-1)/2)
	ret['x_m']           = x_m
	ret['y_m']           = y_m
	ret['z_m']           = z_m
	
	Lx, Ly, Lz, base     = get_baselines(ret)
	
	ret['Lx_m']          = Lx
	ret['Ly_m']          = Ly
	ret['Lz_m']          = Lz
	ret['base']          = base
	
	ret['base_min']      = np.nanmin(base)
	ret['base_max']      = np.nanmax(base)

	return ret



## Convert an angle in degrees to a unicode string with appropriate units.
 #
 # params float angle_deg   Angle in degree
 #
 # return string
 # 
 # Version 11/2019
 # Author Hiep Nguyen
 ##
def deg2str(angle_deg):
    """
    Convert an angle in degrees to a unicode string with appropriate units.
    Based on Cormac's code
    """
    
    try:
        angle_deg    = float(angle_deg)
        angle_arcsec = angle_deg*3600.

        if (angle_arcsec < 60.):
            text = u'{:.2f}"'.format(angle_arcsec)
        elif ( (angle_arcsec >= 60.) and (angle_arcsec < 3600.) ):
            text = u"{:.2f}'".format(angle_deg*60.)
        else:
            text = u"{:.2f}\u00B0".format(angle_deg)
        return text

    except Exception:
        return ""







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
	txt = txt.replace('\'','')
	txt = txt.replace('\"','')
	txt = txt.replace('\n',';')
	
	if( txt[-2:] == ';;' ):
		txt = txt[:-2]
	else:
		txt = txt[:-1]
	
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
def exe_cmd(cmd, kwargs):
	print(cmd)
	print(kwargs)
	
	if(cmd == 'atlod'):
		s = mir.atlod( **kwargs )
		print(s.decode("utf-8") )
		print('Finish!!')
		print('Now you can run: uvflag, or uvsplit')
		print('------')
		print()



	if(cmd == 'uvsplit'):
		s = mir.uvsplit( **kwargs )
		print(s.decode("utf-8") )

		out  = kwargs['vis']

		dirs = glob.glob('./*/')
		dirs = glob.glob('*.[0-9][0-9][0-9][0-9]*', recursive=False) # 1 dot and 4 digits: '.[0-9][0-9][0-9][0-9]'

		freqlist = []
		for d in dirs:
			s = d.split('.')
			freqlist.append( s[1] )
		freqlist = set(freqlist)

		for freq in freqlist:
			if not os.path.exists(freq):
			    os.mkdir(freq)

		for d in dirs:
			s = d.split('.')
			shutil.move(d, s[1])

		shutil.rmtree(out)

		print('Finish!!')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: uvflag -> mfcal')
		print('------')
		print()




	if(cmd == 'uvflag'):
		s = mir.uvflag( **kwargs )
		print(s.decode("utf-8") )
		print('Finish!!')
		print('Next: Check data using "uvplt"')
		print('Then: mfcal -> pgflag -> blflag')
		print('------')
		print()

	if(cmd == 'uvspec'):
		s = mir.uvspec( **kwargs )
		print(s.decode("utf-8") )

	if(cmd == 'uvplt'):
		s = mir.uvplt( **kwargs )
		print(s.decode("utf-8") )


	if(cmd == 'mfcal'):
		s = mir.mfcal( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: pgflag -> blflag')
		print('------')
		print()


	if(cmd == 'pgflag'):
		s = mir.pgflag( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('Should do both "pgflag" with stokes=xx,yy and stokes=yy,xx')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: blflag')
		print('------')
		print()




	if(cmd == 'blflag'):
		s = mir.blflag( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: To examine the bandpass solution, plot the antenna banpass functions with "gpplt"')
		print('You may need to update the calibration solution with "mfcal"')
		print('------')
		print()


	if(cmd == 'gpcal'):
		s = mir.gpcal( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'gpcopy'):
		s = mir.gpcopy( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'gpboot'):
		s = mir.gpboot( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'gpaver'):
		s = mir.gpaver( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'uvaver'):
		s = mir.uvaver( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()



	if(cmd == 'invert'):
		s = mir.invert( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'cgdisp'):
		s = mir.cgdisp( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'clean'):
		s = mir.clean( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'restor'):
		s = mir.restor( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()



	if(cmd == 'imfit'):
		s = mir.imfit( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()



	if(cmd == 'imhist'):
		s = mir.imhist( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'imlist'):
		s = mir.imlist( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'impos'):
		s = mir.impos( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()

	if(cmd == 'mfclean'):
		s = mir.mfclean( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()


	if(cmd == 'selfcal'):
		s = mir.selfcal( **kwargs )
		print(s.decode("utf-8") )

		print('Finish!!')
		print('------')
		print()