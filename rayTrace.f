      program rayTrace

c Remove all except rayTracing wrapper
c Routine pulls rayTracing element out from HypoDD v1.3 code
c available from Waldhauser and Ellsworth, 2000.

	implicit none
	include 'rayTrace.inc'

	character	dattim*25
        real            dists(MAXSTA,MAXEVE)
        real            dist1
        real            dlat
        real            dlon
        real            ed_times(MAXSTA,MAXEVE)
        character       eventfile*80
	logical		ex
        character       fn_inp*80
	character	fn_srcpar*80
        integer         fu_ev
        integer		fu_inp
        integer         fu_sta
	integer		i
	integer		j
        integer         l
        character	line*200
	integer		log
	integer		mod_nl
	real		mod_ratio
	real		mod_top(MAXLAY)
	real		mod_v(MAXLAY)
	integer		narguments
	integer		nev
	integer		nsrc
	integer		nsta
        real            PI
	integer		src_cusp(MAXEVE)
	real		src_dep(MAXEVE)
	doubleprecision	src_lat(MAXEVE)
	doubleprecision	src_lon(MAXEVE)
        character       statfile*80
	character	sta_lab(MAXSTA)*7
	real		sta_lat(MAXSTA)
	real		sta_lon(MAXSTA)
	character	str1*60
        real		temp1, temp2, temp3
        real            temp4, temp5, temp6
	real		tmp_ttp(MAXSTA,MAXEVE)
	real		tmp_tts(MAXSTA,MAXEVE)
	real		tmp_xp(MAXSTA,MAXEVE)
	real		tmp_yp(MAXSTA,MAXEVE)
	real		tmp_zp(MAXSTA,MAXEVE)
	integer		trimlen

c--- open log file:
      call freeunit(log)
      open(log,file='rayTrace.log',status='unknown')
      str1= 'starting rayTrace taken from HypoDDv1.3...'
      call datetime(dattim)
      write(6,'(a45,a)') str1, dattim
      write(log,'(a45,a)') str1, dattim

c---- Other output file:      
      fn_srcpar = 'rayTrace.src'

c---- Input file
      narguments = iargc()
      if(narguments.lt.1) then
        write(*,'(/,a)') 'PARAMETER INPUT FILE [rayTrace.inp <ret>]:'
        read(5,'(a)') fn_inp
        if(trimlen(fn_inp).le.1) then
           fn_inp= 'rayTrace.inp'            !default input file name
        else
           fn_inp= fn_inp(1:trimlen(fn_inp))
        endif
      else
          call getarg(1,fn_inp)
      endif
      inquire(FILE=fn_inp,exist=ex)
      if(.not. ex) stop' >>> ERROR OPENING INPUT PARAMETER FILE.'
      
      l=1

c-- Loop to read each parameter lines, skipping comments
      call freeunit (fu_inp)
      open (fu_inp,status='unknown',file=fn_inp,err=998)
210   read (fu_inp,'(a)',end=220) line
      if (line(1:1).eq.'*' .or. line(2:2).eq.'*') goto 210
      if (l.eq.1) read (line,*,err=999) statfile(1:trimlen(statfile))
      if (l.eq.2) read (line,*,err=999) eventfile(1:trimlen(eventfile))
      if (l.eq.3) read (line,*,err=999) mod_nl
      if (l.eq.4) read (line,*,err=999) mod_ratio
      if (l.eq.5) read (line,*,err=999) (mod_top(i),i=1,mod_nl)
      if (l.eq.6) read (line,*,err=999) (mod_v(i),i=1,mod_nl)
      l=l+1
      goto 210
220   close(fu_inp)

c--- Read in Stations
      call freeunit(fu_sta)
      open(fu_sta,status='unknown',file=statfile,err=9999)
      l = 1
230   read (fu_sta,'(a)',end=240) line
      read (line,*,err=1012) sta_lab(l), sta_lat(l), sta_lon(l)
      l = l+1
      goto 230
240   close(fu_sta)
      nsta = l-1

c--- Read in Events
      call freeunit(fu_ev)
      open(fu_ev,status='unknown',file=eventfile,err=9999)
      l = 1
250   read (fu_ev,'(a)',err=9999,end=260) line
      read (line,*,err=1010) temp1, temp2, src_lat(l),
     &   src_lon(l), src_dep(l), temp3, temp4, temp5,
     &   temp6, src_cusp(l)
      l = l+1
      goto 250
260   close(fu_ev)
      nsrc = l-1

c--- calculate travel times  and slowness vectors:
      write(log,'(/,"~ getting partials for ",i5,
     & " stations and ",i5," source(s) ...")') nsta,nsrc
      call partials(fn_srcpar,
     & nsrc,src_cusp,src_lat,src_lon,src_dep,
     & nsta,sta_lab,sta_lat,sta_lon,
     & mod_nl,mod_ratio,mod_v,mod_top,
     & tmp_ttp,tmp_tts,
     & tmp_xp,tmp_yp,tmp_zp,dists)

      goto 1001

c ---- Error handling
998   write(*,*)'>>> ERROR OPENING CONTROL PARAMETER FILE'
      goto 1000
999   write (*,*)'>>> ERROR READING CONTROL PARAMETERS IN LINE '
      write (*,*) line
      goto 1000
9999  write (*,*) '>>> ERROR OPENING OR READING EVENT OR STATION FILE'
      goto 1000
1010  write (*,*) '** Bad earthquake data, so stop:'
      write (*,*) line
      goto 1000
1012  write (*,*) '** Bad station line, stop:'
      write (*,*) line
1000  write (*,*) '>>> END OF PROGRAM'

1001  end !of main routine
