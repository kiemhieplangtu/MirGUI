## get arguments of a command
 #
 # params str fname   command
 #
 # return str txt     content of the file
 # 
 # Version 1/2020
 # Author Hiep Nguyen
 ##
def exe_cmd(prj, cmd, kwargs):
	# print(cmd)
	# print(kwargs)
	
	if(cmd == 'atlod'):
		try:
			s = mir.atlod( **kwargs )
			s = s.decode("utf-8"); print(s)

			print('Finish - '+ cmd + ' !')
			print('Now you can run: uvflag, or uvsplit')
			print('------')
			print()
		except Exception as e:
			s = e
			print('Error! \n')



	if(cmd == 'uvsplit'):
		try:
			s = mir.uvsplit( **kwargs )
			s = s.decode('utf-8'); print(s)

			dirs = glob.glob('./*/')
			dirs = glob.glob('*.[0-9][0-9][0-9][0-9]*', recursive=False) # 1 dot and 4 digits: '.[0-9][0-9][0-9][0-9]'

			freqlist = []
			for d in dirs:
				spl = d.split('.')
				freqlist.append( spl[1] )
			freqlist = set(freqlist)

			for freq in freqlist:
				frpath = 'projects/'+prj+'/'+freq
				if os.path.exists( frpath ):
				    shutil.rmtree( frpath )
				if not os.path.exists(freq):
				    os.mkdir(freq)

			for d in dirs:
				spl = d.split('.')
				shutil.move(d, spl[1])

			# shutil.rmtree( kwargs['vis'] ) # Remove the oupu file

			for d in freqlist:
				shutil.move( d, 'projects/'+prj+'/' )

			print('Finish - '+ cmd + ' !')
			print('Next: Look at data using "uvplt", "uvspec"')
			print('Then: uvflag -> mfcal')
			print('------')
			print()
		except Exception as e:
			s = e
			print('Error! \n')




	if(cmd == 'uvflag'):
		s = mir.uvflag( **kwargs )
		s = s.decode("utf-8"); print(s)
		print('Finish - '+ cmd + ' !')
		print('Next: Check data using "uvplt"')
		print('Then: mfcal -> pgflag -> blflag')
		print('------')
		print()

	if(cmd == 'uvspec'):
		s = mir.uvspec( **kwargs )
		s = s.decode("utf-8"); print(s)

	if(cmd == 'uvplt'):
		s = mir.uvplt( **kwargs )
		s = s.decode("utf-8"); print(s)


	if(cmd == 'mfcal'):
		s = mir.mfcal( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: pgflag -> blflag')
		print('------')
		print()


	if(cmd == 'pgflag'):
		s = mir.pgflag( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('Should do both "pgflag" with stokes=xx,yy and stokes=yy,xx')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: blflag')
		print('------')
		print()




	if(cmd == 'blflag'):
		s = mir.blflag( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('Next: Look at data using "uvplt", "uvspec"')
		print('Then: To examine the bandpass solution, plot the antenna banpass functions with "gpplt"')
		print('You may need to update the calibration solution with "mfcal"')
		print('------')
		print()


	if(cmd == 'gpcal'):
		s = mir.gpcal( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'gpcopy'):
		s = mir.gpcopy( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'gpboot'):
		s = mir.gpboot( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'gpaver'):
		s = mir.gpaver( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'uvaver'):
		s = mir.uvaver( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()



	if(cmd == 'invert'):
		s = mir.invert( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'cgdisp'):
		s = mir.cgdisp( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'clean'):
		s = mir.clean( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'restor'):
		s = mir.restor( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()



	if(cmd == 'imfit'):
		s = mir.imfit( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()



	if(cmd == 'imhist'):
		s = mir.imhist( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'uvcat'):
		s = mir.uvcat( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'imlist'):
		s = mir.imlist( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'impos'):
		s = mir.impos( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()

	if(cmd == 'mfclean'):
		s = mir.mfclean( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()


	if(cmd == 'selfcal'):
		s = mir.selfcal( **kwargs )
		s = s.decode("utf-8"); print(s)

		print('Finish - '+ cmd + ' !')
		print('------')
		print()

	return s