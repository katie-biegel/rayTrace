CMD	= rayTrace
CC	= gcc
FC	= gfortran
SRCS	= $(CMD).f \
          delaz2.f direct1.f freeunit.f \
	  partials.f refract.f tiddid.f \
	  trimlen.f ttime.f vmodel.f
CSRCS	= atoangle.c datetime_.c
OBJS	= $(SRCS:%.f=%.o) $(CSRCS:%.c=%.o)
INCLDIR	= include
CFLAGS	= -O -I$(INCLDIR)
FFLAGS	= -I$(INCLDIR)

all: $(CMD)

$(CMD): $(OBJS)
	$(FC) $(LDFLAGS) $(OBJS) $(LIBS) -o $@

%.o: %.f
	$(FC) $(FFLAGS) -c $(@F:.o=.f) -o $@

# Extensive lint-like diagnostic listing (SUN f77 only)
rayTrace.lst: $(SRCS)
	f77 -e -Xlist -c $(SRCS)

clean:
	-rm -f $(CMD) *.o core a.out *.fln junk

# Include-file dependencies
rayTrace.o	: $(INCLDIR)/rayTrace.inc
partials.o	: $(INCLDIR)/rayTrace.inc
refract.o	: $(INCLDIR)/rayTrace.inc
tiddid.o	: $(INCLDIR)/rayTrace.inc
ttime.o		: $(INCLDIR)/rayTrace.inc
vmodel.o	: $(INCLDIR)/rayTrace.inc
datetime_.o	: $(INCLDIR)/f77types.h

