

FUNCTION run_daemon, i
host='http://localhost:8022'
url_request=host+'/request/imaging/task/last'
url_post=host+"/request/imaging/task/update"
obj = IDLnetUrl()
i=0

WHILE (1 ne 0) DO BEGIN
	i++
	print, url_request
	json= wget(url_request,/string_array)
	data=JSON_PARSE(json,/TOSTRUCT)
	wait, 1
	i++
	if (data.pending eq 0) then  begin
		wait, 10
		continue
	endif
	resp="_id="+string(data._id)+"&idl_status=started"
	ret=obj->Put(resp, /buffer, /post, url=url_post)

   CATCH, Error_status
 
   ;This statement begins the error handler:
   IF Error_status NE 0 THEN BEGIN
      PRINT, 'Error index: ', Error_status
      PRINT, 'Error message: ', !ERROR_STATE.MSG
      ; Handle the error by extending A:
		resp="_id="+string(data._id)+"&idl_status=failed&error="+!ERROR_STATE.MSG
		ret=obj->Put(resp, /buffer, /post, url=url_post)
	  continue
      CATCH, /CANCEL
   ENDIF
 

	data_folder=data.idl_config.folder
	outfile_prefix=data.idl_config.folder+"/"+data.idl_config.prefix
	if ~file_exist(data_folder) then file_mkdir, data_folder

	log_file=outfile_prefix+"_log.txt"
	openw,lun,log_file,/get_lun
	printf,lun, json
	close, lun
	free_lun, lun

	sig_fname=data.filename
	bkg_fname=data.background.filename

	time_range=data.utc_range
	;filename_prefix=data.get('filename_prefix')

	path_sci_file=data.filename
	path_bkg_file=data.background.filename

	start_utc=data.utc_range[0]
	end_utc=data.utc_range[1]

	bp_elow=6
	bp_ehigh=10

	elow=data.energy_range[0]
	ehigh=data.energy_range[1]

	print, "Processing "+string(data._id)

	aux=data.aux
	L0=aux.L0
	B0=aux.B0
	RSUN=aux.rsun
	dsun=aux.dsun

	require_nonthermal=data.require_nonthermal
	thermal_only=data.thermal_only
	;require_nonthermal=1

	; STIX pointing offsets have opposite signs

	resp="_id="+string(data._id)
	if (data.signal_data_type  eq "PixelData") then begin
		roll_angle=aux.roll
		x_offset_arcsec=  aux.sun_center[0]
		y_offset_arcsec=  aux.sun_center[1]    

		vis_fwdfit_source_type= data.idl_config.fwdfit_shape ; multi or ellipse
		if vis_fwdfit_source_type eq 'multi' then begin
			vis_fwdfit_source_type= ['circle','circle']
		endif
		bp_fname=outfile_prefix + "_bp_map.fits" 
		full_disk_bp_fname=outfile_prefix + "_full_disk_bp_map.fits" 
		vis_fwdfit_fname=outfile_prefix + "_vis_fwdfit_map.fits" 
		em_fname=outfile_prefix + "_em_map.fits"
		clean_fname=outfile_prefix + "_clean_map.fits"

		print, bp_fname+','+full_disk_bp_fname

		stx_image_reconstruct, path_bkg_file, path_sci_file, $
			start_utc, end_utc, $
			elow, ehigh, $
			bp_elow, bp_ehigh, $
			full_disk_bp_fname,  $
			bp_fname, $
			vis_fwdfit_fname, vis_fwdfit_source_type, $
			em_fname, $
			clean_fname,  $
			L0, B0, RSUN, roll_angle, dsun, $
			x_offset_arcsec, y_offset_arcsec, 0
		resp+="&image_bp="+bp_fname+"&image_fwdfit="+vis_fwdfit_fname+"&image_em="+em_fname+"&image_clean="+clean_fname+"&image_full_disk="+full_disk_bp_fname
	endif

	print, "Performing spectral fitting..."
	spectral_fitting_results_filename=outfile_prefix+"_ospex_results.fits"
	result=stx_ospex_pipeline_wrapper(path_sci_file,  path_bkg_file, start_utc,  end_utc, require_nonthermal,thermal_only, spectral_fitting_results_filename)

	print, "writing meta data to database"
	resp+="&idl_status=success&ospex_results="+spectral_fitting_results_filename
	
	ret=obj->Put(resp, /buffer, /post, url=url_post)
	print, "done"
	print, "Executing image creator..."
	SPAWN, "/usr/bin/python3 /opt/stix/parser/stix/flare_pipeline/plot_idl.py " + string(data._id)
ENDWHILE 
return, 1
END




